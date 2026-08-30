from langgraph.graph import StateGraph, START, END    
from typing import TypedDict, Any
from gc_agent.models.fetcher_models import Assignment
from pydantic import BaseModel, Field 
from pprint import pprint
from langchain_google_genai import ChatGoogleGenerativeAI
from gc_agent.agent.system_prompt import SYS_TASK_EXTRACTION_PROMPT, HUMAN_TASK_EXTRACTION_PROMPT, SYS_TASK_COMPLETION_PROMPT, HUMAN_TASK_COMPLETION_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()



model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=7,
)

class Task(BaseModel):
    task: str = Field(
        description="A concise summary of a specific sub-task or deliverable required by the assignment."
    )
    instructions: str = Field(
        description="Detailed, step-by-step guidelines or specific constraints extracted for completing this single task."
    )


class ExtractedTask(BaseModel):
    tasks: list[Task] = Field(
        description="An itemized list of all discrete actionable tasks identified in the assignment document."
    )
    instructions: str = Field(
        description="Overarching instructions, global constraints, formatting rules, or submission guidelines that apply to the entire assignment."
    )
    

class Extraction(BaseModel):
    task: ExtractedTask = Field(
        description="Structured extraction of discrete sub-tasks and overarching instructions."
    )
    globalinstructions: list[str] = Field(
        description="A list of explicit global constraints, rules, and guidelines."
    )
    format: str = Field(
        description="The target deliverable format required for completion (e.g., 'Executable Python Script using Matplotlib', 'Jupyter Notebook (.ipynb)')."
    )

class State(TypedDict):
    id:str
    title:str
    description:str
    pdf_text:list[str]
    task: ExtractedTask
    upload_format:str
    global_inst:list[str]
    completed_task:str
    
def extract_task(state: State) -> dict[str, Any]:
    # `State` is a TypedDict, so LangGraph supplies it as a regular dict at
    # runtime rather than an object with attributes.
    task_extraction_message = [
    SystemMessage(content = SYS_TASK_EXTRACTION_PROMPT),
    HumanMessage(content = HUMAN_TASK_EXTRACTION_PROMPT.format(**state))
    ]

    llm = model.with_structured_output(Extraction)
    extraction = llm.invoke(task_extraction_message)

    return {"task":extraction.task, "upload_format":extraction.format, "global_inst":extraction.globalinstructions} 


def complete_task(state: State) -> dict[str, ExtractedTask]:
    task_extraction_message = [
    SystemMessage(content = SYS_TASK_COMPLETION_PROMPT),
    HumanMessage(content = HUMAN_TASK_COMPLETION_PROMPT.format(**state))
    ]

    completed_task = model.invoke(task_extraction_message)
    print(completed_task)
    return {"completed_task":completed_task.content} 

      
builder = StateGraph(State)
builder.add_node("extractor", extract_task)
builder.add_node("completion", complete_task)

# 4. Set entry and finish points
builder.add_edge(START, "extractor")
builder.add_edge("extractor", "completion")
builder.add_edge("completion", END)

# 5. Compile the graph
agent = builder.compile()
  


