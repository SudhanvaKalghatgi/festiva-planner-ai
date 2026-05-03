from src.ml.budget_model import (
    load_data,
    preprocess_data,
    train_model,
    predict_budget,
)


def test_model_training():
    df = load_data()
    X, y, _ = preprocess_data(df)

    model = train_model(X, y)

    assert model is not None


def test_prediction_output():
    sample_input = {
        "guest_count": 200,
        "city_tier": 1,
        "event_type": "wedding",
        "season": 1,
        "lead_time_days": 90,
        "has_live_music": 1,
        "has_alcohol": 1,
        "is_outdoor": 1,
        "is_destination": 0,
    }

    result = predict_budget(sample_input)

    assert isinstance(result, dict)
    assert len(result) == 8

    total = sum(result.values())

    # Allow small floating error
    assert 0.95 <= total <= 1.05