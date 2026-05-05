from src.ml.input_parser import parse_query
from src.ml.budget_model import predict_budget
from src.agents.knowledge_agent import knowledge_agent
from src.agents.conflict_agent import conflict_agent


def generate_plan(query: str):
    # 🔥 Step 1: Parse user input
    parsed = parse_query(query)

    # 🔥 Step 2: Predict budget split
    budget_percentages = predict_budget(parsed)

    # 🔥 Step 3: Convert percentages → amounts
    total_budget = parsed.get("budget", 0)

    budget_split = {}
    for category, pct in budget_percentages.items():
        amount = int(pct * total_budget)
        budget_split[category] = {
            "percentage": pct,
            "amount": amount
        }

    # 🔥 Step 4: Plan object
    plan = {
        "parsed_input": parsed,
        "budget_split": budget_split
    }

    # 🔥 Step 5: Knowledge (slightly improved trigger)
    knowledge = None
    if any(k in query.lower() for k in ["timeline", "plan", "how", "guide", "steps"]):
        knowledge = knowledge_agent(query)

    # 🔥 Step 6: Conflicts
    conflicts = conflict_agent(plan)

    # 🔥 Step 7: Return final
    return {
        "plan": plan,
        "knowledge": knowledge,
        "conflicts": conflicts
    }