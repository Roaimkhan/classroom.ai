from gc_agent.Oauth.authentication_client import authenticate
from gc_agent.fetcher.utils import pdf_bytes_to_text
from gc_agent.fetcher.fetcher import gc_fetcher
from gc_agent.llm.llm import run_llm
from googleapiclient.discovery import build
from gc_agent.parser.parser import separate_tasks_assignments
from pathlib import Path 
from typing import Any
import json
from gc_agent.dir import DATA_DIR
from pprint import pprint 


ASSGINMENT_MATERIAL_DIR = DATA_DIR/"assignment_material"

##----THE BELOW CODE IS ONLY FOR TESTING AT THE MOMENT
def file_id_unwrapper(materials:list[dict[str,Any]]) -> list[str]:
    urwrap_file_ids = []
    for material in materials:
        if next(iter(material)) == "driveFile":
            urwrap_file_ids.append(material.get("driveFile","null"))
    return urwrap_file_ids


def build_fetcher():
    creds = authenticate()
    clsrm_client = build("classroom", "v1", credentials=creds)
    dr_client = build("drive", "v3", credentials=creds)
    fetcher = gc_fetcher(clsrm_client,dr_client)
    return fetcher

def get_courses_ids():
    with open(DATA_DIR/"registered.json","r") as file:
        courses = json.load(file)
    print(courses)
    course_ids = []
    for course in courses:
        course_ids.append(course.get("courseId"))
    return course_ids
    

def main():
    fetcher = build_fetcher()

    fetcher.update_courses()
    registered_courses_id = get_courses_ids()

    ASSGINMENT_MATERIAL_DIR.mkdir(parents=True, exist_ok=True)
    for course_id in registered_courses_id:
        print(f"\n\n\n\nTHIS IS COURSE {course_id}")
    
        assignment = fetcher.get_assignments(course_id)
        due_assignments = assignment.get("without_duedate",{})
 
        for i in due_assignments:
            assignmt_materials = i.get("materials",{})
            file_ids = file_id_unwrapper(assignmt_materials)
            print(i.get("title"))

            for id in file_ids:
                pdf_bytes = fetcher.download_assignments(id)
                text = pdf_bytes_to_text(pdf_bytes)
                text = separate_tasks_assignments(text)
                print(text)
                pprint(run_llm(text))
                break

                 

if __name__ == "__main__":
    main()
