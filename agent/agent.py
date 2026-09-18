from langgraph.graph import StateGraph, START, END    
from typing import TypedDict, Any
from gc_agent.models.fetcher_models import Assignment
from pydantic import BaseModel, Field 
from pprint import pprint
from langchain_groq import ChatGroq
from gc_agent.agent.system_prompt import SYS_TASK_EXTRACTION_PROMPT, HUMAN_TASK_EXTRACTION_PROMPT, SYS_TASK_COMPLETION_PROMPT, HUMAN_TASK_COMPLETION_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from gc_agent.agent.file_generator import generate_cpp
import os
load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",  # You can also use "llama-3.1-8b-instant" for faster tasks
    api_key=os.getenv("GROQ_API_KEY"),  # Pulls your Groq key from .env
    temperature=0.7
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
        description="The target deliverable format required for completion. It must strictly be strictly filled with the required file format end (e.g., '.py', '.cpp', '.pdf')."
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

def package_task(state: State):
    
    format = state["upload_format"]
    print(f"========================{format}=========================")
    match format:
        case ".cpp":
            print("=========file format matched=======================")
            generate_cpp(state["completed_task"],format)
    


builder = StateGraph(State)
builder.add_node("extractor", extract_task)
builder.add_node("completion", complete_task)
builder.add_node("package_task", package_task)
# 4. Set entry and finish points
builder.add_edge(START, "extractor")
builder.add_edge("extractor", "completion")
builder.add_edge("completion", "package_task")
builder.add_edge("package_task", END)

# 5. Compile the graph
agent = builder.compile()
  


if __name__ == "__main__":
    package_task({
        "upload_format":".cpp",
        "completed_task":"""
                        #include <iostream> // Header library for input and output streams

                        int main() {
                            // Print text to the screen
                            std::cout << "Hello, World!" << std::endl; 
                            
                            return 0; // Indicates the program finished successfully
                        }    
        """
    })
