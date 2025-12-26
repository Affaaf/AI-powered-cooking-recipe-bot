from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from .base import AgentState
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

def create_llm_router() -> ChatOpenAI:
    """Create an LLM instance for routing decisions"""
    return ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

def should_continue(state: AgentState) -> str:
    """
    Use LLM to determine the next step in the workflow based on the current state.
    Returns either 'continue' or 'end' based on the LLM's decision.
    """
    llm = create_llm_router()
    
    # Create a system message explaining the routing task
    system_message = SystemMessage(content="""You are a workflow router for a recipe assistant.
    Based on the current state, determine if the workflow should continue or end.
    Consider:
    1. If the user's query is cooking-related
    2. If we have sufficient information to proceed
    3. If the user's request has been fully addressed
    
    Respond with either 'continue' or 'end' only.""")
    
    # Create a human message with the current state
    human_message = HumanMessage(content=f"""Current state:
    Query: {state['query']}
    Is cooking related: {state['is_cooking']}
    Cookware verified: {state['cookware_ok']}
    
    Should the workflow continue or end?""")
    
    # Get the LLM's decision
    response = llm.invoke([system_message, human_message])
    decision = response.content.strip().lower()
    
    # Ensure we get a valid response
    if decision not in ['continue', 'end']:
        return 'continue'
   
    return decision