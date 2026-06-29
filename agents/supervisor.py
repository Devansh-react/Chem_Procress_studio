from utils.schema import ReactionState as State
from langchain.tools import tool
from langchain.agents import create_agent
from utils.llm import get_gemini_model as model
model = model()
from agents.explainer import explainer_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents import create_agent
from deepagents.middleware.filesystem import FilesystemMiddleware


middleware_list = [
    
    
]

subagents = [
    {
        "name": "",
        "description": "This subagent can get",
        "system_prompt": "",
        "tools": [],
        "model": model,
        "middleware": [],
    },
]


middleware_list = [
    HumanInTheLoopMiddleware(
        interrupt_on={
            
        }
    )
    
    
]



supervisor_agent = create_agent(
    model = model,
    system_prompt = "...."  
    subagents = subagents,
    middleware= middleware_list
)