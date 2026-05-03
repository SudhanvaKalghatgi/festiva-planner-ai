from src.ml.pipeline import generate_plan


def test_pipeline():
    text = "Wedding in Bangalore for 200 guests with live music"

    result = generate_plan(text)

    assert "parsed_input" in result
    assert "budget_split" in result

    split = result["budget_split"]

    assert isinstance(split, dict)
    assert len(split) == 8

    total = sum(split.values())
    assert 0.95 <= total <= 1.05