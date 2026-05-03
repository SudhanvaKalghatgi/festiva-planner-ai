from src.ml.pipeline import generate_plan


def planner_agent(query: str):
    result = generate_plan(query)

    return {
        "type": "plan",
        "data": result
    }