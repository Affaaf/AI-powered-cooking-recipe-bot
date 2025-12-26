import sys
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .base import AgentState

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def classify_query_node(state: AgentState) -> AgentState:
    """Node to classify if the query is cooking-related using LangChain's LLM"""
    llm = ChatOpenAI(temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that determines if a query is cooking-related. Respond with 'yes' or 'no' only."),
        ("user", "Is this query cooking-related? Query: {query}")
    ])
    
    query = state.get("query", "")
    
    formatted_prompt = prompt.format_messages(query=query)
    response = llm.invoke(formatted_prompt)
    
    is_cooking = response.content.lower().strip() == "yes"
    
    state["is_cooking"] = is_cooking
    print(f"Inside Classify Query Node: is_cooking: {state['is_cooking']}")
    return state 