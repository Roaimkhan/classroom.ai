from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime
from googleapiclient.discovery import build
from gc_agent.fetcher.utils import CTime , retry_decorator
from gc_agent.custom_errors import gc_error_mapper
from gc_agent.dir import DATA_DIR 
from gc_agent.Oauth.authentication_client import authenticate
from datetime import datetime
import io
import asyncio
import json
from pprint import pprint
from typing import  Any
from pydantic import BaseModel, Field , TypeAdapter

class Assignment(BaseModel):
    id: str
    title: str
    courseId: str
    description: str | None = None
    driveId: dict[str, Any] = Field(default_factory=dict)
    dueDate: datetime | None = None
    materials: list[Any] = Field(default_factory=list)

class ALLassignments(BaseModel):
    assignments :list[Assignment]

AssignmentListValidator = TypeAdapter(list[Assignment])

class gc_fetcher:
    """
    Service wrapper for Google Classroom and Google Drive APIs.

    Handles metadata synchronization, assignment parsing, material extraction,
    and binary file downloads for Google Classroom courses.

    Attributes:
        clsrm_client (Resource): Authenticated Google Classroom API service client.
        dr_client (Resource): Authenticated Google Drive API service client.

    Methods:
        update_courses():
            Fetches all enrolled courses for the authenticated user and caches 
            a mapping of course IDs and names to 'registered.json'.

        get_assignments(courseId: str) -> dict[str, list[dict[str, Any]]]:
            Retrieves and categorizes coursework for a given course ID into
            'due_assignments', 'not_due_assignments', and 'without_duedate'.

        download_assignments(file_id: str) -> bytes:
            Downloads a target Google Drive file or exports Google Docs as PDFs,
            returning the raw byte array content for downstream parsing.
    """

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
        
        with open(DATA_DIR/"registered_courses.json","w") as file:
            json.dump(cl_courses,file)

    def _clean_assignmt_provided(self,asignmt:dict)->list[dict[str,Any]]:
        _materials = []
        for j in asignmt.get("materials", []):
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
            assgnmnt_list.append(Assignment(
                            id=single_assgnmt.get("id"),
                            title=single_assgnmt.get("title"),
                            courseId=single_assgnmt.get("courseId"),
                            description=single_assgnmt.get("description"),
                            driveId=single_assgnmt.get("driveId", {}),
                            materials=materials,
                            ))
        else:
            assgnmnt_list.append(Assignment(
                            id=single_assgnmt.get("id"),
                            title=single_assgnmt.get("title"),
                            courseId=single_assgnmt.get("courseId"),
                            description=single_assgnmt.get("description"),
                            driveId=single_assgnmt.get("driveId", {}),
                            materials=materials,
                            dueDate=single_assgnmt.get("dueDate",{}),
            ))
            
    @retry_decorator(retry_range = 3)
    async def get_assignments(self,courseId:str)->dict[str, list[dict[str, Any]]]:
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
        assignments = assignments.get("courseWork", []) 
        # pprint(assignments)
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
                single_assgnmt["dueDate"] = due_time
                if not all_assignments.get("due_assignments",[]):
                    all_assignments["due_assignments"] = []
                self._make_final_assignmt(all_assignments.get("due_assignments",[]),single_assgnmt,materials)
                
            elif due_time > ctime.current_time():
                single_assgnmt["dueDate"] = due_time
                if not all_assignments.get("not_due_assignments",[]):
                    all_assignments["not_due_assignments"] = []
                self._make_final_assignmt(all_assignments.get("not_due_assignments",[]),single_assgnmt,materials)
        
        return all_assignments
    
    async def fetch_all_Assignments(self)-> ALLassignments:
        path = DATA_DIR / "registered_courses.json"
        with open(path) as file :
            data = json.load(file)
            tasks = []
            async with asyncio.TaskGroup() as tg:
                for course in data:
                    courseId = course.get("courseId","")
                    if courseId == "":
                        print(f"course id not found for course {course.name}")
                        continue
                    task = tg.create_task(self.get_assignments(courseId))
                    tasks.append(task)

        all_fetched = [
            assignment 
            for task in tasks 
            for result_dict in [task.result()] 
            if isinstance(result_dict, dict)
            for assignment_list in result_dict.values() 
            if assignment_list
            for assignment in assignment_list
        ]
        final_Assignments = ALLassignments(assignments=all_fetched)
        # for i in  final_Assignments.assignments:
        #     print(f"{i}\n")
        return final_Assignments


                    
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


def build_fetcher()->gc_fetcher:
    creds = authenticate()
    clsrm_client = build("classroom", "v1", credentials=creds)
    dr_client = build("drive", "v3", credentials=creds)
    fetcher = gc_fetcher(clsrm_client,dr_client)
    return fetcher

if __name__ == "__main__":
    fetcher = build_fetcher()
    fetcher.update_courses()
    pprint(fetcher.get_assignments("850051495510"))
