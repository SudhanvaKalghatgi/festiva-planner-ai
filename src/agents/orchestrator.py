from src.agents.planner_agent import planner_agent
from src.agents.knowledge_agent import knowledge_agent
from src.agents.output_engine import generate_final_output

def orchestrator(query: str):
    query_lower = query.lower()

    response = {}

    # 🔥 Planner trigger (ONLY when user wants planning/budget)
    if any(word in query_lower for word in ["budget", "cost", "estimate", "price"]) \
       or ("plan" in query_lower and "how" not in query_lower):
        response["plan"] = planner_agent(query)["data"]

    # 🔥 Knowledge trigger (info queries)
    if any(word in query_lower for word in ["how", "what", "timeline", "guide"]):
        response["knowledge"] = knowledge_agent(query)

    # 🔥 If query clearly asks for both
    if "plan" in query_lower and any(word in query_lower for word in ["timeline", "how"]):
        response["plan"] = planner_agent(query)["data"]
        response["knowledge"] = knowledge_agent(query)

    # 🔥 Fallback
    if not response:
        response["knowledge"] = knowledge_agent(query)

    formatted = generate_final_output(response)

    return {
    "query": query,
    "response": formatted["formatted_response"],
    "raw": formatted["raw"]
}