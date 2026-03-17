from googleapiclient.discovery import build
from gc_agent.fetcher.fetcher import gc_fetcher
from gc_agent.Oauth.authentication_client import authenticate
import json
from pprint import pprint 
from pathlib import Path 


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

##----THE BELOW CODE IS ONLY FOR TESTING AT THE MOMENT
def main():
    creds = authenticate()
    service = build("classroom", "v1", credentials=creds)
    fetcher = gc_fetcher(service)
    fetcher.get_courses()
    with open(DATA_DIR/"registered.json","r") as file:
            courses = json.load(file)
    course = courses[0]
    assignment = fetcher.get_assignments(course)
    pprint(assignment)


if __name__ == "__main__":
    main()
