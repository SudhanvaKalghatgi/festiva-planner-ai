from src.ml.reallocation import reallocate_budget


def test_reallocation():
    sample = {
        "venue": 0.25,
        "catering": 0.30,
        "decor": 0.10,
        "photography": 0.10,
        "music": 0.05,
        "invites": 0.05,
        "transport": 0.10,
        "contingency": 0.05,
    }

    updated = reallocate_budget(sample, "add live music")

    assert isinstance(updated, dict)
    assert len(updated) == 8

    total = sum(updated.values())
    assert 0.99 <= total <= 1.01

    assert updated["music"] > sample["music"]