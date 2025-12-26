import sys
import os
from typing import List

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .base import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def verify_cookware_node(state: AgentState) -> AgentState:
    """Node to verify if user has required cookware"""
    AVAILABLE_COOKWARE = [
        "Spatula", "Frying Pan", "Little Pot", "Stovetop",
        "Whisk", "Knife", "Ladle", "Spoon"
    ]
    
    # Get the recipe from state
    recipe = state["recipe"]
    recipe_text = recipe
    
    # Create LLM prompt to analyze recipe compatibility
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a cooking expert. Analyze if the given recipe can be cooked with the available cookware.
         If it is a simple recipe, you can cook it with the available cookware, output YES. Only respond with NO if the recipe requires cookware that is not available.
        Available cookware: {cookware}
        
        Respond with only 'YES' or 'NO' followed by a brief explanation.
        Example: YES - All required cookware is available
        Example: NO - Missing a blender which is needed for smoothies"""),
        ("user", "Recipe:\n{recipe}")
    ])
    
    # Initialize LLM
    llm = ChatOpenAI(temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    
    # Format the prompt with available cookware and recipe
    formatted_prompt = prompt.format_messages(
        cookware=", ".join(AVAILABLE_COOKWARE),
        recipe=recipe_text
    )
    
    # Get LLM response
    response = llm.invoke(formatted_prompt)
    result = response.content.strip()
    
    # Parse the response
    cookware_ok = result.startswith("YES")
    state["cookware_ok"] = cookware_ok
    state["cookware_analysis"] = result
    
    print(f"Inside Verify Cookware Node: response: {state['cookware_ok']}")
    return state 