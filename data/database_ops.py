from gc_agent.data.database_models import AssignmentDB, session
from gc_agent.fetcher.fetcher import ALLassignments

def writetodb(assignment:ALLassignments)->None:
    n=1
    for assgn in assignment.assignments:
        try:
            asgnt = AssignmentDB(**assgn.model_dump())
            session.add(asgnt)
        except:
            raise(f"Couldnt write assignment{n}  to database")
        n+=1

    session.commit()
