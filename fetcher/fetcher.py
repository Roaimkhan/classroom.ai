from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime
from gc_agent.models.fetcher_models import Course, Assignment, ALLassignments, ALLcourses
from gc_agent.fetcher.utils import CTime , retry_decorator
from gc_agent.custom_errors import gc_error_mapper
from gc_agent.dir import DATA_DIR 
from datetime import datetime
import io
import asyncio
import json
from pprint import pprint
from typing import Any


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
    async def update_courses(self)->ALLcourses:
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

        _courses = results.get("courses", [])
        if not _courses:
            print("No courses found.")

        processed_courses = []
        for course in _courses:  
            temp = Course(**course)
            processed_courses.append(temp)
        
        return ALLcourses(courses=processed_courses)


    def _extract_materials(self,asignmt:dict)->list[dict[str,Any]]:
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
    
    async def _make_final_assignmt(self,
                            assgnmnt_list:list,
                            single_assgnmt:dict,
                            materials:list,
                            dueDate = True,
                            ) -> None:
        print(f"DEBUG: materials type is {type(materials)}")
        # Import at the point of use to keep the fetcher independent of the
        # database write service during application startup.
        from gc_agent.data.database_ops import getCourseNameFrmDb

        courseId = single_assgnmt.get("courseId")
        coursename = await getCourseNameFrmDb(courseId)
        print(f"===================================={coursename}=============================================================================")
        if not dueDate:
            assgnmnt_list.append(Assignment(
                            id=single_assgnmt.get("id"),
                            title=single_assgnmt.get("title"),
                            courseId=courseId,
                            coursename=coursename,
                            description=single_assgnmt.get("description"),
                            driveId=single_assgnmt.get("driveId", {}),
                            materials=materials,
                            due_date_status=single_assgnmt.get("due_date_status")
                            ))
        else:
            assgnmnt_list.append(Assignment(
                            id=single_assgnmt.get("id"),
                            title=single_assgnmt.get("title"),
                            courseId=courseId,
                            coursename=coursename,
                            description=single_assgnmt.get("description"),
                            driveId=single_assgnmt.get("driveId", {}),
                            materials=materials,
                            dueDate=single_assgnmt.get("dueDate",{}),
                            due_date_status=single_assgnmt.get("due_date_status")
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
        assignments = self.clsrm_client.courses().courseWork().list(courseId=courseId).execute()
        assignments = assignments.get("courseWork", []) 
        all_assignments = {}
        ctime = CTime
        for single_assgnmt in assignments:
            
            materials = self._extract_materials(single_assgnmt)

            if not single_assgnmt.get("dueDate",[]):
                single_assgnmt["due_date_status"] = "WithoutDueDate"
                if not all_assignments.get("without_duedate",[]):
                    all_assignments["without_duedate"] = []
                await self._make_final_assignmt(all_assignments.get("without_duedate",[]),single_assgnmt,materials,dueDate = False)
                continue

            due_time = ctime.format_time(single_assgnmt.get("dueDate",{}),single_assgnmt.get("dueTime",{})) 
            if due_time <= ctime.current_time():
                single_assgnmt["dueDate"] = due_time
                single_assgnmt["due_date_status"] = "Due"
                if not all_assignments.get("due_assignments",[]):
                    all_assignments["due_assignments"] = []
                await self._make_final_assignmt(all_assignments.get("due_assignments",[]),single_assgnmt,materials)
                
            elif due_time > ctime.current_time():
                single_assgnmt["dueDate"] = due_time
                single_assgnmt["due_date_status"] = "Pending"
                if not all_assignments.get("not_due_assignments",[]):
                    all_assignments["not_due_assignments"] = []
                await self._make_final_assignmt(all_assignments.get("not_due_assignments",[]),single_assgnmt,materials)
        
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
