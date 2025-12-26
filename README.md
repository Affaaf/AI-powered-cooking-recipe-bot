# AI-powered cooking recipe assistant built with LangGraph and Google Search Agent

## Prerequisites

- Python 3.9 or higher

## Setup Instructions

1. Clone the repository:
```bash
git clone AI-powered-cooking-recipe-bot
cd AI-powered-cooking-recipe-bot
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file and add enviroment variables:
# sample .env
```bash
OPENAI_API_KEY = "Your OPENAI API key"
SERPER_API_KEY = "Your SERPER API key"
```
## Running the API

1. Start the API server:
```bash
# Make sure you're in the project root directory
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

2. Access the API documentation:
- Swagger UI: `http://localhost:8000/docs`

## Docker Support

Alternatively, you can run the application using Docker:

1. Build the Docker image:
```bash
docker build -t fastapi-app .
```

2. Run the container:
```bash
docker run --env-file .env -p 8000:8000 fastapi-app
```
## Usage
Sample queries to test:
- Can you help me make pasta?
- Who is the president of the US?
- Can you help me make a burger using just this cookware:  Spatula, Frying Pan, Little Pot, Stovetop, Whisk, Knife, Ladle, Spoon?


## API Endpoints

The API provides the following endpoints:

- `/graph`: Endpoint for graph visualization
- Additional endpoints can be found in the API documentation

## Development

- The API is built using FastAPI
- The main application code is located in the `backend` directory
- Graph-related functionality is in the `backend/graph` directory
