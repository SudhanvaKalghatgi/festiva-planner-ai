from fastapi import FastAPI
from pydantic import BaseModel

from src.ml.pipeline import generate_plan
from src.agents.knowledge_agent import knowledge_agent
from src.agents.orchestrator import orchestrator

app = FastAPI(title="Festiva Planner AI")


# -----------------------------
# Request Models
# -----------------------------
class QueryRequest(BaseModel):
    query: str


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Festiva Planner AI is running"}


# -----------------------------
# Planner Endpoint (ML + Pipeline)
# -----------------------------
@app.post("/plan")
def create_plan(request: QueryRequest):
    result = generate_plan(request.query)
    return result


# -----------------------------
# Knowledge Endpoint (RAG)
# -----------------------------
@app.post("/knowledge/query")
def knowledge_query(request: QueryRequest):
    result = knowledge_agent(request.query)
    return result

@app.post("/assistant")
def assistant(request: QueryRequest):
    result = orchestrator(request.query)
    return result