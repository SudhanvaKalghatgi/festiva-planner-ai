from fastapi import FastAPI
from pydantic import BaseModel

from src.ml.pipeline import generate_plan
from src.agents.knowledge_agent import knowledge_agent
from src.agents.output_engine import generate_final_output
from src.agents.polish_agent import polish_response

app = FastAPI(title="Festiva Planner AI")


# -----------------------------
# Request Model
# -----------------------------
class QueryRequest(BaseModel):
    query: str


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"message": "Festiva Planner AI is running"}


# -----------------------------
# Main Planner (FULL PIPELINE)
# -----------------------------
@app.post("/plan")
def create_plan(request: QueryRequest):
    raw_result = generate_plan(request.query)

    # 🔥 Format output
    formatted = generate_final_output(raw_result)

    # 🔥 Polish using Gemini
    polished_text = polish_response(formatted["formatted_response"])

    return {
        "query": request.query,
        "response": polished_text,
        "raw": formatted["raw"]
    }


# -----------------------------
# Knowledge (RAG)
# -----------------------------
@app.post("/knowledge/query")
def knowledge_query(request: QueryRequest):
    return knowledge_agent(request.query)