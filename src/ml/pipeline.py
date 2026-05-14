from src.ml.input_parser import parse_query
from src.ml.budget_model import predict_budget

from src.agents.knowledge_agent import knowledge_agent
from src.agents.conflict_agent import conflict_agent
from src.agents.recommendation_agent import recommendation_agent
from src.agents.negotiation_agent import negotiation_agent

def generate_plan(query: str):

    # -----------------------------------
    # 🔥 Step 1: Parse User Input
    # -----------------------------------
    parsed = parse_query(query)

    # -----------------------------------
    # 🔥 Step 2: Predict Budget Split
    # -----------------------------------
    budget_percentages = predict_budget(parsed)

    # -----------------------------------
    # 🔥 Step 3: Convert Percentages → Amounts
    # -----------------------------------
    total_budget = parsed.get("budget", 0)

    budget_split = {}

    for category, pct in budget_percentages.items():

        amount = int(pct * total_budget)

        budget_split[category] = {
            "percentage": round(float(pct), 3),
            "amount": amount
        }

    # -----------------------------------
    # 🔥 Step 4: Build Plan Object
    # -----------------------------------
    plan = {
        "parsed_input": parsed,
        "budget_split": budget_split
    }

    # -----------------------------------
    # 🔥 Step 5: Knowledge Agent Trigger
    # -----------------------------------
    knowledge = None

    knowledge_keywords = [
        "timeline",
        "plan",
        "how",
        "guide",
        "steps",
        "budget",
        "venue",
        "catering",
        "decor",
        "destination",
        "wedding",
        "corporate",
        "event",
        "photography",
        "vendors"
    ]

    query_lower = query.lower()

    if any(keyword in query_lower for keyword in knowledge_keywords):
        knowledge = knowledge_agent(query)

    # -----------------------------------
    # 🔥 Step 6: Conflict Analysis
    # -----------------------------------
    conflicts = conflict_agent(plan)

    # -----------------------------------
    # 🔥 Step 7: Recommendation Engine
    # -----------------------------------
    recommendations = recommendation_agent(
        plan,
        conflicts
    )

    negotiation = negotiation_agent(plan)

    # -----------------------------------
    # 🔥 Step 8: Final Response
    # -----------------------------------
    return {
        "plan": plan,
        "knowledge": knowledge,
        "conflicts": conflicts,
        "recommendations": recommendations,
        "negotiation": negotiation
    }