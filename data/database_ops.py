from gc_agent.data.database_models import CourseDB, AssignmentDB, AsyncSessionLocal
from gc_agent.models.fetcher_models import ALLassignments, ALLcourses
from gc_agent.fetcher.fetcher_factory import build_fetcher
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert as pg_insert

def get_current_user():
    ...


# WRITING DATA TO DATABASE


async def updateAssgnDb()->None:
    fetcher = build_fetcher()
    all_assgn = await fetcher.fetch_all_Assignments()
    await _writeAssgntodb(all_assgn)


async def updateCoursesDb():
     fetcher = build_fetcher()
     all_courses = await fetcher.update_courses()
     await _writeCoursestodb(all_courses)


async def _writeAssgntodb(assignment:ALLassignments)->None:
    try:
        payload = [assgn.model_dump() for assgn in assignment.assignments ]

        if not payload:
            return 
        
        async with AsyncSessionLocal() as db:
            async with db.begin():
                stmt = pg_insert(AssignmentDB).values(payload)
                stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
                await db.execute(stmt)

    except Exception as e:
        raise RuntimeError(f"Couldn't write assignments to database at item {e}")
    
async def _writeCoursestodb(courses:ALLcourses)->None:
    try:
        payload = [course.model_dump() for course in courses.courses]
        async with AsyncSessionLocal() as db:
            async with db.begin():
                stmt = pg_insert(CourseDB).values(payload)
                stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
                await db.execute(stmt)
    except Exception as e:
            raise RuntimeError(f"Couldn't write assignments to database at item {e}")



# QUERING DATA FROM DATABASE


async def getPendingAssgnFrmDb():
    async with AsyncSessionLocal() as db:
        stmt = select(AssignmentDB).where(AssignmentDB.due_date_status == "WithoutDueDate")
        result_scalars = await db.scalars(stmt)
        results = result_scalars.all()
        return results
    
async def getPendingAssgnCountFrmDb():
    # current_user = get_current_user(token)
    async with AsyncSessionLocal() as db:
        stmt = select(func.count(AssignmentDB.id)).where(AssignmentDB.due_date_status == "Pending")
        return await db.scalar(stmt) or 0


async def getCourseNameFrmDb(courseid:str):
    async with AsyncSessionLocal() as db:
        stmt = select(CourseDB.name).where(CourseDB.id == courseid)
        return await db.scalar(stmt)

async def getCoursesFrmDb():
    async with AsyncSessionLocal() as db:
            stmt = select(CourseDB)
            res =  await db.scalars(stmt)
            return res.all()
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(updateCoursesDb())