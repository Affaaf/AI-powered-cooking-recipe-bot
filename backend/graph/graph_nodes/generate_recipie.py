import sys
import os
from typing import Dict, Any
from dotenv import load_dotenv
from .base import AgentState
from langchain_core.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.messages import HumanMessage
from langchain_openai import OpenAI
from langchain.agents import initialize_agent
import json

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def generate_recipe_node(state: AgentState) -> AgentState:
    """Node to generate recipe with optional web search."""
    
    if not state["is_cooking"]:
        state["response"] = "I'm sorry, I can only assist with cooking and recipe-related queries."
        return state

    dish = state["query"]
    messages = [HumanMessage(dish)]

    llm = OpenAI(temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    search = GoogleSerperAPIWrapper()
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="call this tool to search the web for recipe information",
        )
    ]
    try:
        self_ask_with_search = initialize_agent(
            tools, llm, verbose=True, handle_parsing_errors=True
        )
        response = self_ask_with_search.invoke(
            f"""You are a professional chef and cooking expert. 
         Generate a precise, step-by-step recipe that is easy to follow.
         Include:
         1. List of ingredients with quantities
         2. Step-by-step cooking instructions
        
         If you need additional information, use the available tools to search the web.
        
         Keep the instructions clear, concise, and beginner-friendly. You have tool attached to search the web.  
         Analyze if you need to use the search tool before generating the recipe. User Question {dish}"""
        )
    except Exception as e:
        print(f"Error in generating recipe: {e}")
        state["recipe"] = "I'm sorry, I couldn't generate a recipe for that dish. Please try again with a different dish."

    try:
        state["recipe"] = response["output"] 

    except Exception as e:
        print(f"Error in generating recipe: {e}")
        state["recipe"] = "I'm sorry, I couldn't generate a recipe for that dish. Please try again with a different dish."

    print(f"Inside Generate Recipe Node: recipe: {state['recipe']}")
    return state  
