from src.ml.input_parser import parse_input
from src.ml.budget_model import predict_budget
from src.ml.reallocation import reallocate_budget


def generate_plan(user_input: str):
    # Step 1: Parse input
    parsed = parse_input(user_input)

    # Step 2: Predict budget split
    budget_split = predict_budget(parsed)

    # Step 3: Apply dynamic changes (basic trigger)
    if "music" in user_input.lower():
        budget_split = reallocate_budget(budget_split, "add music")

    # Step 4: Get total budget from parsed input
    total_budget = parsed.get("budget", 1000000)

    # 🔥 Step 5: Convert to exact budget allocation (no rounding loss)

    # Raw amounts
    raw_amounts = {k: v * total_budget for k, v in budget_split.items()}

    # Convert to integers
    int_amounts = {k: int(v) for k, v in raw_amounts.items()}

    # Fix rounding difference
    difference = total_budget - sum(int_amounts.values())

    # Add remaining amount to largest category
    max_key = max(int_amounts, key=int_amounts.get)
    int_amounts[max_key] += difference

    # Final structured output
    detailed_budget = {
        k: {
            "percentage": round(budget_split[k], 3),
            "amount": int_amounts[k],
        }
        for k in budget_split
    }

    return {
        "parsed_input": parsed,
        "budget_split": detailed_budget,
    }


if __name__ == "__main__":
    user_text = "Wedding in Bangalore for 200 guests with 15 lakh budget and live music"

    result = generate_plan(user_text)

    print(result)