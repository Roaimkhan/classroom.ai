from googleapiclient.errors import HttpError
from gc_agent.fetcher.utils import CTime
from gc_agent.custom_errors import gc_error_mapper, GCRConnectionError, GCRServerError, GCRRateLimitError
import time
import json
from pprint import pprint
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def retry_decorator(retry_range=3):
    def decorator(func):
        def wrapper(*args,**kwargs):            
                exponential_factor = 1
                for i in range(retry_range):
                    try:
                        return func(*args,**kwargs)
                    except (GCRConnectionError, GCRServerError):
                        time.sleep(5)
                        print(f"Retry attempt {i+1} failed")
                        
                    except (GCRRateLimitError):
                        time.sleep(5*exponential_factor)
                        exponential_factor += 1
                        print(f"Retry attempt {i+1} failed")

        return wrapper
    return decorator


class gc_fetcher:
    
    def __init__(self,client):
        self.client = client


    @retry_decorator(retry_range = 3)
    def get_courses(self)->None:
        """
            Description:
                This function generates a json file containing a list of all registered courses' of the user with their IDs and names
                i.e:
                    [{"id":"34324234","course_name":"Pre Calculus"},
                    {"id":"34325562","course_name":"OOP"},....  ]
        """
        try:
            results = self.client.courses().list(pageSize=10).execute()
        except HttpError as e:
            error_code = e.resp.status
            raise gc_error_mapper(error_code)

        courses = results.get("courses", [])
        if not courses:
            print("No courses found.")

        cl_courses = []
        for course in courses:  
            cl_courses.append({
                "id" : course["id"],
                "name" : course["name"]
                })
        
        with open(DATA_DIR/"registered.json","w") as file:
            json.dump(cl_courses,file)


    def _clean_assignmt_provided(self,asignmt:dict)->list[dict[str,Any]]:
        _materials = []
        n = 0
        for j in asignmt["materials"]:
            if (next(iter(j))=="driveFile"):
                drive_info = j.get("driveFile",{}).get("driveFile",{})
                _materials.append({f"driveFile{n}":drive_info.get("id",{})})

            elif(next(iter(j))=="youtubeVideo"):
                _materials.append({"youtubeVideoLink":j.get("youtubeVideo").get("alternateLink")})

            elif(next(iter(j))=="link"):
                _materials.append({"Link":j.get("link").get("url")})
                    
            n+=1
        return _materials
    
    def _make_final_assignmt(self,
                            all_assignments:list,
                            assignment_typ:str,
                            single_assgnmt:dict,
                            materials:list,
                            dueDate = True,
                            ) -> None:
        if not dueDate:
            all_assignments[assignment_typ] = {
                            "title" :single_assgnmt.get("title",),
                            "description":single_assgnmt.get("description",{}),
                            "driveId":single_assgnmt.get("driveId",{}),
                            "materials":materials,
                            }
        else:
            all_assignments[assignment_typ] = {
                            "title" :single_assgnmt.get("title",),
                            "description":single_assgnmt.get("description",{}),
                            "driveId":single_assgnmt.get("driveId",{}),
                            "dueDate":single_assgnmt.get("dueDate",{}),
                            "materials":materials,
                            }

    def get_assignments(self,course:dict)->dict[str, list[dict[str, Any]]]:
        """
            Description:
                This function returns a list containing all the assignments for a given course !
                Puts them in three different dicts:
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
        courseId = course["id"]
        assignments = self.client.courses().courseWork().list(courseId=courseId).execute()
        assignments = assignments.get("courseWork") 
        # "assignments" is basically list of all the assignments uploaded to that particular coure
        all_assignments = {}
        pprint(assignments)

        ctime = CTime
        for i in assignments:
            materials = self._clean_assignmt_provided(i)

            if not i.get("dueDate",[]):
                print("without_duedate executed")
                if not all_assignments.get("without_duedate",[]):
                    all_assignments["without_duedate"] = []
                self._make_final_assignmt(all_assignments,"without_duedate",i,materials,dueDate = False)
                continue

            due_time = ctime.format_time(i.get("dueDate",{}),i.get("dueTime",{})) 
            if due_time > ctime.current_time():
                print("due_assignments executed")
                if not all_assignments.get("due_assignments",[]):
                    all_assignments["due_assignments"] = []
                self._make_final_assignmt(all_assignments,"due_assignments",i,materials)
                
            elif due_time < ctime.current_time():
                print("not_due_assignments executed")
                if not all_assignments.get("not_due_assignments",[]):
                    all_assignments["not_due_assignments"] = []
                self._make_final_assignmt(all_assignments,"not_due_assignments",i,materials)

        return all_assignments