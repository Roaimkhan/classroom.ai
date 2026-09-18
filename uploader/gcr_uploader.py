from googleapiclient.discovery import build
from gc_agent.Oauth.authentication_client import authenticate

# 1. Initialize your Classroom service wrapper
# service = build('classroom', 'v1', credentials=credentials)
creds = authenticate()
clsrm_client = build("classroom", "v1", credentials=creds)

def _get_submission_id(course_id,assignment_id,user_id):
    # STEP 1: Find your unique student submission ID for this assignment
    # Passing "-" as the userId tells Google to look for the currently logged-in student
    submissions_response = clsrm_client.courses().courseWork().studentSubmissions().list(
        courseId=course_id,
        courseWorkId=assignment_id,
        userId="-" 
    ).execute()

    submissions = submissions_response.get('studentSubmissions', [])

    if not submissions:
        print("No submission slot found. Are you enrolled as a student in this course?")
    else:
        submission_id = submissions[0]['id']
        print(f"Found your unique submission slot ID: {submission_id}")

if __name__ == "__main__":
    _get_submission_id()


    
def submit_assignment(course_id,assignment_id,user_id):
    # STEP 2: Attach your file or link to the submission
    # Let's say you want to attach a website link or a Google Drive file link
    submission_id = _get_submission_id(course_id,assignment_id,user_id)
    attachment_payload = {
        "attachments": [
            {
                "link": {       
                    "url": "https://my-homework-sharing-site.com",
                    "title": "My Completed Essay"
                }
            }
        ]
    }
    # Upload/modify the submission attachments
    updated_submission = clsrm_client.courses().courseWork().studentSubmissions().modifyAttachments(
        courseId=course_id,
        courseWorkId=assignment_id,
        id=submission_id,
        body=attachment_payload
    ).execute()
    print("✅ Successfully uploaded/attached your file to the assignment!")

def turnin_assignment(course_id,assignment_id,user_id):
        # STEP 3: Officially click "Turn In"
        # This changes the status from 'CREATED' to 'SUBMITTED' so the teacher can see it
        clsrm_client.courses().courseWork().studentSubmissions().turnIn(
            courseId=course_id,
            courseWorkId=assignment_id,
            id=submission_id,
            body={} # Body is empty for the turnIn action
        ).execute()
        print("🚀 Assignment officially Turned In!")
