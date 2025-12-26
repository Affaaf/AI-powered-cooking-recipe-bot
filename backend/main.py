import logging
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage
from graph.recipe_graph import create_recipe_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI-Powered Recipe Chatbot")

class QueryRequest(BaseModel):
    query: str

@app.post("/api/cooking")
async def handle_query(request: QueryRequest):
    query = request.query.strip()
    logger.info(f"Received query: {query}")

    try:
        # Initialize the graph
        graph = create_recipe_graph()
        
    
    # Create initial state with proper message handling
        initial_state = {
            "query": query,
            "is_cooking": False,
            "recipe": "",  # Initialize empty recipe
            "cookware_ok": False,
            "response": ""
        }
        
        # Run the graph
        final_state = graph.invoke(initial_state)
        return {"response": final_state["response"]}
    except Exception as e:
        logger.exception("Error processing query")
        raise HTTPException(status_code=500, detail="Internal Server Error")
