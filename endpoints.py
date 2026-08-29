from gc_agent.dir import DATA_DIR
# from gc_agent.agent.AssignmentDispatcher import AssignmentDispatcher
from gc_agent.fetcher.fetcher_factory import build_fetcher
from gc_agent.database.database_models import engine, init_db
from gc_agent.database.database_ops import updateAssgnDb, getPendingAssgnCountFrmDb, _writeAssgntodb, getPendingAssgnFrmDb, updateCoursesDb, getCoursesFrmDb, getAssgnFrmDbThruId
import asyncio
import json
from pprint import pprint
from contextlib import asynccontextmanager
from fastapi import FastAPI
path = DATA_DIR / "registered_courses.json"


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
    assgn = await getPendingAssgnFrmDb()
    print(assgn)
    return {"all_pending_assgn": assgn}

@app.get("/refresh")
async def refresh():
    await updateCoursesDb()
    courses = await getCoursesFrmDb()
    await updateAssgnDb()
    assgn = await getPendingAssgnFrmDb()
    return {"all_pending_assgn": assgn,"registered_courses":courses}

@app.post("/assignments/{assignment_id}/complete")
async def completeAssignment(assignment_id:str):
    assgn = await AssignmentDispatcher(assignment_id)
    # assgn = await getAssgnFrmDbThruId(assignment_id)
    return {"assignment":assgn}



if __name__ == "__main__":
    fetcher = build_fetcher()
    assignments = asyncio.run(fetcher.fetch_all_Assignments())
    # pprint(assignments.model_dump())
    asyncio.run(_writeAssgntodb(assignments))
