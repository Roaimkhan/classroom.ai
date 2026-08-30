from gc_agent.database.database_ops import getAssgnFrmDbThruId
from gc_agent.fetcher.fetcher_factory import fetcher
from gc_agent.agent.utils import pdf_bytes_to_text
from gc_agent.agent.agent import agent
import asyncio


async def AssignmentDispatcher(id:str):
    # GET RELEVANT MATERIALS
    assignment = await getAssgnFrmDbThruId(id)
    if not assignment.materials:
        print("no attachments found for this assignment")
    else:
        materials = assignment.materials
        file_ids = [i.get("driveFile","") for i in materials]
        print(f"""
            FILE IDS :{file_ids}
        """)

    # DOWNLOAD THE MATERIAL
    if file_ids:
        downloaded_files = [fetcher.download_assignments(id) for id in file_ids]

    
    # PARSE THEM FOR THE AGENT
    parsed_files:list[str] = [pdf_bytes_to_text(file) for file in  downloaded_files]
    print(f"""
            FILES IN TEXT :{parsed_files[0]}
        """)

    # PASS IT TO THE AGENT
    title = ""
    if assignment.title:
        title = assignment.title

    description = ""
    if assignment.description:
        description = assignment.description
    
    assignment = {
        "id": id,
        "title":title,
        "description":description,
        "pdf_text":parsed_files
    }

    agent.invoke(assignment)

if __name__ == "__main__":
    asyncio.run(AssignmentDispatcher("857029995043"))