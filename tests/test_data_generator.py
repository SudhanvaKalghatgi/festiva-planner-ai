from src.ml.data_generator import generate_dataset

def test_dataset_generation():
    df = generate_dataset(100)

    assert not df.empty
    assert "city" in df.columns
    assert "budget" in df.columns
    assert len(df) == 100