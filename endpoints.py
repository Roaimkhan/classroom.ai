from gc_agent.dir import DATA_DIR
from gc_agent.fetcher.fetcher import build_fetcher
import asyncio
import json

from fastapi import FastAPI
path = DATA_DIR / "registered_courses.json"
fetcher = build_fetcher()


if __name__ == "__main__":
    
    asyncio.run(fetcher.fetch_all_Assignments())