from src.ml.input_parser import parse_input


def test_parse_input():
    text = "Wedding in Bangalore for 300 guests with outdoor setup and live music"

    result = parse_input(text)

    assert result["event_type"] == "wedding"
    assert result["city"] == "bangalore"
    assert result["guest_count"] == 300
    assert result["is_outdoor"] == 1
    assert result["has_live_music"] == 1