from langgraph import STATEGRAPH, START, END    
from typing import TypedDict
from gc_agent.models.fetcher_models import Assignment



class State(TypedDict):
    asssignment:Assignment



def start(state:State):
    
