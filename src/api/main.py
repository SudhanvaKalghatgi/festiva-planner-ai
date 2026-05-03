from fastapi import FastAPI
from pydantic import BaseModel

from src.ml.pipeline import generate_plan


app = FastAPI()


class PlanRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "Festiva Planner AI is running"}


@app.post("/plan")
def create_plan(request: PlanRequest):
    result = generate_plan(request.query)
    return result