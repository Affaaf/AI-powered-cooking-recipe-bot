from typing import Dict, TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    query: str
    is_cooking: bool
    recipe: str
    cookware_ok: bool
    response: str 
    cookware_analysis: str