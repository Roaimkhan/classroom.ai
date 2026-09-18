from gc_agent.dir import DATA_DIR
from gc_agent.agent.AssignmentDispatcher import AssignmentDispatcher
from gc_agent.fetcher.fetcher_factory import build_fetcher
from gc_agent.database.database_models import engine, init_db
from gc_agent.database.database_ops import updateAssgnDb, getPendingAssgnCountFrmDb, _writeAssgntodb, getUserPendingAssgnFrmDb, updateCoursesDb, updateUserCourses, getUserCoursesFrmDb, getAssgnFrmDbThruId, checkAssignmentStatus
import asyncio
import json
import jwt
from pprint import pprint
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Security  # Ensure Security is here!
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redis import Redis
from rq import Queue
path = DATA_DIR / "registered_courses.json"
import os
from dotenv import load_dotenv
from jwt import PyJWKClient

# Load environment variables from .env file
load_dotenv()

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
JWKS_URL = f"{SUPABASE_PROJECT_URL}/auth/v1/.well-known/jwks.json"



security = HTTPBearer()


# Initialize the JWK client to fetch and cache public keys
jwks_client = PyJWKClient(JWKS_URL)

def verify_supabase_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        # Dynamically fetch the correct public key using the 'kid' in the token header
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        # Decode and verify using the ES256 algorithm and the public key
        payload = jwt.decode(
            token, 
            signing_key.key, 
            algorithms=["ES256", "RS256"], # Supports modern Supabase asymmetric keys
            options={"verify_aud": False}
        )
        
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
        
    except Exception as e:
        print(f"JWT Verification Error: {e}")
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose() 

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

@app.get("/getPendingassgn")
async def getPendingAssgn():
    await updateAssgnDb()
    assgn = await getPendingAssgnCountFrmDb()
    print(assgn)
    return {"total_pending_assgn": assgn}

@app.get("/fetchPendingAssignments")
async def fetchPendingAssignments():
    await updateAssgnDb()
    assgn = await getUserPendingAssgnFrmDb()
    print(assgn)
    return {"all_pending_assgn": assgn}

@app.get("/refresh")
async def refresh(user_id: str = Depends(verify_supabase_token)):
    await updateCoursesDb()
    await updateUserCourses(user_id)
    courses = await getUserCoursesFrmDb(user_id)
    await updateAssgnDb()
    assgn = await getUserPendingAssgnFrmDb(user_id)
    return {"all_pending_assgn": assgn,"registered_courses":courses}

# The completeAssignment endpoint creates a job record 
# in the database and dispatches the assignment to the 
# Redis/RQ queue, then immediately returns a job_id to 
# the frontend. A background worker picks up the job and 
# processes the assignment asynchronously, updating its 
# status in the database (queued → processing → completed/failed).
# The frontend uses the GET /jobs/{job_id} status endpoint to 
# check the job's progress and display the current state to the user.

redis_conn = Redis(host="localhost", port=6379)
task_queue = Queue("task_queue", connection = redis_conn)

@app.post("/assignments/{assignment_id}/complete")
async def completeAssignment(assignment_id:str):
    # incase assignment is completed by some other user
    # we show the user a slightly modified copy of the
    # already completed assignment rather than recreating it from scratch 
    updateAssignmentStatus("InProgresse",assignment_id)
    job = task_queue.enqueue(AssignmentDispatcher, assignment_id)
    return {
        "completion_status":"InProgresse",
        "job":job.id,
        "message": f"Assignment {assignment_id} sent to background queue!",
    }

async def poolAssignmentStatus(assignment_id:str):
    status = checkAssignmentStatus(assignment_id)
    return {
        "completion_status":status,
    }


if __name__ == "__main__":
    fetcher = build_fetcher()
    assignments = asyncio.run(fetcher.fetch_all_Assignments())
    # pprint(assignments.model_dump())
    asyncio.run(_writeAssgntodb(assignments))
