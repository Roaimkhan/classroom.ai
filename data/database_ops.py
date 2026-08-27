from gc_agent.data.database_models import AssignmentDB, AsyncSessionLocal
from gc_agent.fetcher.fetcher import ALLassignments
from gc_agent.fetcher.fetcher import build_fetcher
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert as pg_insert

def get_current_user():
    ...


async def updateAssgnDb()->None:

    """
    Function for fetching all assignments
    from classroom and writing them to the
    database. It aviods writing duplicate ones
    """

    fetcher = build_fetcher()
    all_assgn = await fetcher.fetch_all_Assignments()
    await _writetodb(all_assgn)


async def getPendingAssgnCountFrmDb():
    # current_user = get_current_user(token)
    async with AsyncSessionLocal() as db:
        stmt = select(func.count(AssignmentDB.id)).where(AssignmentDB.due_date_status == "WithoutDueDate")
        return await db.scalar(stmt) or 0

async def _writetodb(assignment:ALLassignments)->None:
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