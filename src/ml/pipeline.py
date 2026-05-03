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

    return {
        "parsed_input": parsed,
        "budget_split": budget_split,
    }


if __name__ == "__main__":
    user_text = "Wedding in Bangalore for 200 guests with outdoor setup and live music"

    result = generate_plan(user_text)

    print(result)