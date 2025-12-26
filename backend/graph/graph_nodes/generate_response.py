import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .base import AgentState

# Load environment variables
load_dotenv()

def generate_response_node(state: AgentState) -> AgentState:
    """Node to generate the final response using LLM"""
    if not state["is_cooking"]:
        state["response"] = "I'm sorry, I can only assist with cooking and recipe related queries."
        print(f"Inside Generate Response Node: response: {state['response']}")
        return state
    
    elif not state["cookware_ok"]:
        state["response"] = "It appears you do not have the necessary cookware to prepare this dish. The following cookware is missing: " + state["cookware_analysis"] + "\n" + "However, Here is the recipe: " + state["recipe"]
        print(f"Inside Generate Response Node: response: {state['response']}")
        return state
    else:
        llm = ChatOpenAI(
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o",
        )
        prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a professional chef and cooking expert. 
        Generate a precise, step-by-step recipe that is easy to follow.
        Include:
        1. List of ingredients with quantities
        2. Step-by-step cooking instructions
        
        If you need additional information, use the available tools to search the web.
        
        Keep the instructions clear, concise, and beginner-friendly. You have tool attached to search the web.  
        Here is the response from the search tool: {state["recipe"]}"""),

        ("user", "Please provide a brief recipe for: {dish}")
        ])

        formatted_prompt = prompt.format_messages(dish = state["query"])

        response = llm.invoke(formatted_prompt)
        state["response"] = response.content

        print(f"Inside Generate Response Node: response: {state['response']}")
        return state 