from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from gc_agent.fetcher.utils import CTime
from gc_agent.custom_errors import gc_error_mapper, GCRConnectionError, GCRServerError, GCRRateLimitError
from gc_agent.dir import DATA_DIR 
import io
import time
import json
from pprint import pprint
from pathlib import Path
from typing import Any


def retry_decorator(retry_range=3):
    def decorator(func):
        def wrapper(*args,**kwargs):            
                exponential_factor = 1
                for attempt in range(retry_range):
                    try:
                        return func(*args,**kwargs)
                    except (GCRConnectionError, GCRServerError) as e:
                        if (attempt == retry_range):
                            raise e
                        time.sleep(5)
                        print(f"Retry attempt {attempt+1} failed")
                      
                    except (GCRRateLimitError) as e:
                        if (attempt == retry_range):
                            raise e
                        time.sleep(5*exponential_factor)
                        exponential_factor += 1
                        print(f"Retry attempt {attempt+1} failed")

        return wrapper
    return decorator


class gc_fetcher:
    
    def __init__(self,clsrm_client,dr_client):
        self.clsrm_client = clsrm_client
        self.dr_client = dr_client

    @retry_decorator(retry_range = 3)
    def update_courses(self)->None:
        """
            Description:
                This function generates a json file containing a list of all registered courses' of the user with their courseIds and names
                i.e:
                    [{"courseId":"34324234","course_name":"Pre Calculus"},
                     {"courseId":"34325562","course_name":"OOP"},....  ]
        """
        try:
            results = self.clsrm_client.courses().list(pageSize=10).execute()
        except HttpError as e:
            error_code = e.resp.status
            raise gc_error_mapper(error_code)

        courses = results.get("courses", [])
        if not courses:
            print("No courses found.")

        cl_courses = []
        for course in courses:  
            cl_courses.append({
                "courseId" : course["id"],
                "name" : course["name"]
                })
        
        with open(DATA_DIR/"registered.json","w") as file:
            json.dump(cl_courses,file)

    def _clean_assignmt_provided(self,asignmt:dict)->list[dict[str,Any]]:
        _materials = []
        for j in asignmt.get("materials"):
            if (next(iter(j))=="driveFile"):
                drive_info = j.get("driveFile",{}).get("driveFile",{})
                _materials.append({f"driveFile":drive_info.get("id",{})})

            elif(next(iter(j))=="youtubeVideo"):
                _materials.append({"youtubeVideoLink":j.get("youtubeVideo").get("alternateLink")})

            elif(next(iter(j))=="link"):
                _materials.append({"Link":j.get("link").get("url")})
                    
        return _materials
    
    def _make_final_assignmt(self,
                            assgnmnt_list:list,
                            single_assgnmt:dict,
                            materials:list,
                            dueDate = True,
                            ) -> None:
        if not dueDate:
            assgnmnt_list.append({
                            "title" :single_assgnmt.get("title",),
                            "description":single_assgnmt.get("description",{}),
                            "driveId":single_assgnmt.get("driveId",{}),
                            "materials":materials,
                            })
        else:
            assgnmnt_list.append({
                            "title" :single_assgnmt.get("title",),
                            "description":single_assgnmt.get("description",{}),
                            "driveId":single_assgnmt.get("driveId",{}),
                            "dueDate":single_assgnmt.get("dueDate",{}),
                            "materials":materials,
                            })
    @retry_decorator(retry_range = 3)
    def get_assignments(self,courseId:str)->dict[str, list[dict[str, Any]]]:
        """
            Description:
                This function returns a list containing all the assignments for a given course !
                Puts them in three different buckets:
                    1.due
                    2.not due yet
                    3.without duedate

            Parameters:
                Only takes "courseId"

            i.e:
                get_assignments("34324234")

            returns:

                {"without_duedate":[{"title":"Lab-02",
                                    "driveId": "abc...",
                                    "link": "https://drive...."}],
                "due_assignments":[{"title":"Lab-02",
                                    "driveId": "abc...",
                                    "link": "https://drive...."}],
                "not_due_assignments":[{"title":"Lab-02",
                                    "driveId": "abc...",
                                    "link": "https://drive...."}],
                }
        """
        # courseId = course["id"]
        assignments = self.clsrm_client.courses().courseWork().list(courseId=courseId).execute()
        assignments = assignments.get("courseWork") 
        # "assignments" is basically list of all the assignments uploaded to that particular coure
        all_assignments = {}

        ctime = CTime
        for single_assgnmt in assignments:

            materials = self._clean_assignmt_provided(single_assgnmt)

            if not single_assgnmt.get("dueDate",[]):
                if not all_assignments.get("without_duedate",[]):
                    all_assignments["without_duedate"] = []
                self._make_final_assignmt(all_assignments.get("without_duedate",[]),single_assgnmt,materials,dueDate = False)
                continue

            due_time = ctime.format_time(single_assgnmt.get("dueDate",{}),single_assgnmt.get("dueTime",{})) 
            if due_time < ctime.current_time():
                if not all_assignments.get("due_assignments",[]):
                    all_assignments["due_assignments"] = []
                self._make_final_assignmt(all_assignments.get("due_assignments",[]),single_assgnmt,materials)
                
            elif due_time > ctime.current_time():
                if not all_assignments.get("not_due_assignments",[]):
                    all_assignments["not_due_assignments"] = []
                self._make_final_assignmt(all_assignments.get("not_due_assignments",[]),single_assgnmt,materials)

        return all_assignments
    

    @retry_decorator(retry_range = 3)
    def download_assignments(self,file_id:str):

        """Downloads files from google classroom course
        Args:
            file_id: driveFile of the file to download
        Returns : Text extracted from that file
        """

        def _download(request):
            _file = io.BytesIO()
            downloader = MediaIoBaseDownload(_file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")
            return _file

        try:
            file_metadata = self.dr_client.files().get(fileId=file_id, fields='mimeType').execute()
            file_type = file_metadata.get('mimeType')

            if file_type == "application/vnd.google-apps.document":
                request = self.dr_client.files().export(fileId=file_id, mimeType="application/pdf")
                file = _download(request)
            else:
                request = self.dr_client.files().get_media(fileId=file_id)
                file = _download(request)                

        except HttpError as e:
            file = None
            error_code = e.resp.status
            error = gc_error_mapper(error_code)("couldnt download the pdf")
            raise error
        
        return file.getvalue()
    


if __name__ == "__main__":
    fetcher = gc_fetcher
    fetcher.get_courses()