from gc_agent.database.database_models import UserCourses, CourseDB, AssignmentDB, AsyncSessionLocal
from gc_agent.models.fetcher_models import ALLassignments, ALLcourses
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert as pg_insert

def get_current_user():
    ...

# WRITING DATA TO DATABASE


async def updateAssgnDb()->None:
    from gc_agent.fetcher.fetcher_factory import build_fetcher
    fetcher = build_fetcher()
    all_assgn = await fetcher.fetch_all_Assignments()
    await _writeAssgntodb(all_assgn)


async def updateCoursesDb():
    from gc_agent.fetcher.fetcher_factory import build_fetcher
    fetcher = build_fetcher()
    all_courses = await fetcher.update_courses()
    await _writeCoursestoCourseDB(all_courses)

async def updateUserCourses(userid:str):
    from gc_agent.fetcher.fetcher_factory import build_fetcher
    fetcher = build_fetcher()
    all_courses = await fetcher.update_courses()
    # `update_courses()` returns an ALLcourses model; access its `.courses` list
    course_ids = [c.id for c in all_courses.courses]
    await _writetoUserCourses(userid,course_ids)

async def _writetoUserCourses(userid:str,courseids:list[str]):
    try:
        payload = [{"user_id":userid,"course_id":cid} for cid in courseids]
        if not payload:
            return

        async with AsyncSessionLocal() as db:
                async with db.begin():
                    stmt = pg_insert(UserCourses).values(payload)
                    stmt = stmt.on_conflict_do_nothing(index_elements=["user_id", "course_id"])
                    await db.execute(stmt)

    except Exception as e:
        raise RuntimeError(f"Couldn't write usercourses to database at item {e}")
    

async def _writeAssgntodb(assignment:ALLassignments)->None:
    try:
        payload = [assgn.model_dump() for assgn in assignment.assignments ]

        if not payload:
            return 
        
        async with AsyncSessionLocal() as db:
            async with db.begin():
                stmt = pg_insert(AssignmentDB).values(payload)
                update_dict = {
                    "title": stmt.excluded.title,
                    "course_id":stmt.excluded.course_id,
                    "coursename": stmt.excluded.coursename,
                    "description": stmt.excluded.description,
                    "materials": stmt.excluded.materials,
                    "dueDate": stmt.excluded.dueDate,
                    "due_date_status": stmt.excluded.due_date_status,
                }
                stmt = stmt.on_conflict_do_update(index_elements=["id"],set_=update_dict)
                await db.execute(stmt)

    except Exception as e:
        raise RuntimeError(f"Couldn't write assignments to database at item {e}")
    
async def _writeCoursestoCourseDB(courses:ALLcourses)->None:
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


async def getUserPendingAssgnFrmDb(userid:str):
    async with AsyncSessionLocal() as db:
        stmt = (
            select(AssignmentDB)
            .join(UserCourses , UserCourses.course_id == AssignmentDB.course_id)
            .where(AssignmentDB.due_date_status == "Pending",
                   UserCourses.user_id == userid)
        )
        result_scalars = await db.scalars(stmt)
        results = result_scalars.all()
        return results
    
async def getAssgnFrmDbThruId(id:str):
    async with AsyncSessionLocal() as db:
        stmt = select(AssignmentDB).where(AssignmentDB.id == id)
        return await db.scalar(stmt)

async def getPendingAssgnCountFrmDb():
    # current_user = get_current_user(token)
    async with AsyncSessionLocal() as db:
        stmt = select(func.count(AssignmentDB.id)).where(AssignmentDB.due_date_status == "Pending")
        return await db.scalar(stmt) or 0


async def getCourseNameFrmDb(courseid:str):
    async with AsyncSessionLocal() as db:
        stmt = select(CourseDB.name).where(CourseDB.id == courseid)
        return await db.scalar(stmt)

async def getUserCoursesFrmDb(userid:str):
    async with AsyncSessionLocal() as db:
            stmt = (
                select(CourseDB)
                .join(UserCourses, CourseDB.id == UserCourses.course_id)
                .where(UserCourses.user_id == userid)
            )
            res =  await db.scalars(stmt)
            return res.all()

async def getCourselist():
    async with AsyncSessionLocal() as db:
        stmt = select(CourseDB.id)
        res = await db.scalars(stmt)
        return res.all()

    
if __name__ == "__main__":
    import asyncio
    asyncio.run(getCourselist())