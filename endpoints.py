from gc_agent.dir import DATA_DIR
from gc_agent.fetcher.fetcher import build_fetcher
from gc_agent.data.database_ops import writetodb
import asyncio
import json
from pprint import pprint
from fastapi import FastAPI
path = DATA_DIR / "registered_courses.json"
fetcher = build_fetcher()


if __name__ == "__main__":
    
    assignments = asyncio.run(fetcher.fetch_all_Assignments())
    writetodb(assignments)
    # pprint(assignments.model_dump())