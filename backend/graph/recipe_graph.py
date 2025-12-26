from langgraph.graph import Graph, StateGraph
import logging
import os
import sys
from typing import Dict, Any, List, Annotated
from typing_extensions import Annotated

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.graph_nodes import (
    AgentState,
    classify_query_node,
    generate_recipe_node,
    verify_cookware_node,
    generate_response_node,
)
from graph.graph_nodes.llm_router import should_continue
from langchain_core.messages import HumanMessage, AIMessage

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,   # Log level (INFO, WARNING, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Example usage
logger = logging.getLogger(__name__)

# Create the graph
def create_recipe_graph() -> Graph:
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("classify", classify_query_node)
    workflow.add_node("generate_recipe", generate_recipe_node)
    workflow.add_node("verify_cookware", verify_cookware_node)
    workflow.add_node("generate_response", generate_response_node)

    # Add edges
    # workflow.add_edge("classify", START)
    workflow.add_edge("generate_recipe", "verify_cookware")
    # workflow.add_edge("search", "verify_cookware")
    workflow.add_edge("verify_cookware", "generate_response")

    # Add conditional edges
    workflow.add_conditional_edges(
        "classify", should_continue, {"continue": "generate_recipe", "end": "generate_response"}
    )

    # Set entry point
    workflow.set_entry_point("classify")
    workflow.set_finish_point("generate_response")

    return workflow.compile()


def visualize_graph(output_dir: str = "graph_visualization") -> str:

    graph = create_recipe_graph()
    graph_image = graph.get_graph().draw_mermaid_png()

    # Save the image
    output_path = os.path.join(output_dir, "recipe_graph.png")
    with open(output_path, "wb") as f:
        f.write(graph_image)

    logger.info(f"Graph visualization saved to: {output_path}")
    return output_path


def test_flow(user_query: str) -> Dict[str, Any]:
    """
    Test the recipe assistant flow with a given user query.
    
    Args:
        user_query (str): The user's input query
        
    Returns:
        Dict[str, Any]: The final state of the workflow including the response
    """
    # Initialize the graph
    graph = create_recipe_graph()
    
    # Create initial state with proper message handling
    initial_state = {
        "query": user_query,
        "is_cooking": False,
        "recipe": "",  # Initialize empty recipe
        "cookware_ok": False,
        "response": ""
    }
    
    try:
        # Execute the graph
        final_state = graph.invoke(initial_state)
        
        logger.info(f"Query: {user_query}")
        logger.info(f"Final response: {final_state['response']}")
        
        return final_state
    except Exception as e:
        logger.error(f"Error executing graph: {str(e)}")
        raise

# if __name__ == "__main__":
#     # Example usage
#     test_queries = [
#         # "How do I make pasta?",
#         "Can you help me cook pasta?"
#         # "Who is the president of the United States?"
#     ]
    
#     for query in test_queries:
#         # print(f"\nTesting query: {query}")
#         try:
#             result = test_flow(query)
#             # print(f"Response: {result['response']}")
#         except Exception as e:
#             print(f"Error: {str(e)}")
#         print("-" * 50)

# visualize_graph()
