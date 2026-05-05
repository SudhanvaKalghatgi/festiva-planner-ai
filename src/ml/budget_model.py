import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor


DATA_PATH = "data/raw/events.csv"
MODEL_PATH = "models/budget_model.joblib"


# -------------------------------
# TRAINING
# -------------------------------

def load_data():
    return pd.read_csv(DATA_PATH)


def preprocess_data(df):
    X = df[
        [
            "guest_count",
            "city_tier",
            "event_type",
            "season",
            "lead_time_days",
            "has_live_music",
            "has_alcohol",
            "is_outdoor",
            "is_destination",
        ]
    ]

    y = df[
        [
            "venue_pct",
            "catering_pct",
            "decor_pct",
            "photography_pct",
            "music_pct",
            "invites_pct",
            "transport_pct",
            "contingency_pct",
        ]
    ]

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    event_encoded = encoder.fit_transform(X[["event_type"]])

    event_df = pd.DataFrame(
        event_encoded,
        columns=encoder.get_feature_names_out(["event_type"]),
    )

    X = X.drop(columns=["event_type"]).reset_index(drop=True)
    X = pd.concat([X, event_df], axis=1)

    return X, y, encoder


def train_model(X, y):
    model = MultiOutputRegressor(
        XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
        )
    )
    model.fit(X, y)
    return model


def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Mean Absolute Error: {mae:.4f}")


def save_model(model, encoder):
    joblib.dump({"model": model, "encoder": encoder}, MODEL_PATH)
    print(f"Model saved at {MODEL_PATH}")


# -------------------------------
# INFERENCE
# -------------------------------

def load_model():
    bundle = joblib.load(MODEL_PATH)
    return bundle["model"], bundle["encoder"]


def _prepare_dataframe(input_data):
    """
    Accept dict OR DataFrame and normalize into single-row DataFrame
    """
    if isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
    elif isinstance(input_data, dict):
        df = pd.DataFrame([input_data])
    else:
        raise ValueError("Input must be dict or DataFrame")

    return df


def predict_budget(input_data):
    model, encoder = load_model()

    # 🔥 FIX: normalize input (no double wrapping)
    df = _prepare_dataframe(input_data)

    # 🔥 Drop unused column if present
    if "city" in df.columns:
        df = df.drop(columns=["city"])

    # 🔥 Encode event_type safely
    if "event_type" not in df.columns:
        raise ValueError("Missing 'event_type' in input")

    event_encoded = encoder.transform(df[["event_type"]])
    event_df = pd.DataFrame(
        event_encoded,
        columns=encoder.get_feature_names_out(["event_type"]),
    )

    df = df.drop(columns=["event_type"]).reset_index(drop=True)
    df = pd.concat([df, event_df], axis=1)

    # 🔥 Align columns with training schema
    expected_columns = model.estimators_[0].feature_names_in_

    # Add missing columns
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    # Remove extra columns
    df = df[expected_columns]

    # 🔥 Predict
    preds = model.predict(df)[0]

    # 🔥 Normalize safely
    total = preds.sum()
    if total == 0:
        preds = np.ones_like(preds) / len(preds)
    else:
        preds = preds / total

    preds = [float(x) for x in preds]

    categories = [
        "venue",
        "catering",
        "decor",
        "photography",
        "music",
        "invites",
        "transport",
        "contingency",
    ]

    return dict(zip(categories, preds))


# -------------------------------
# TRAIN ENTRYPOINT
# -------------------------------

def main():
    df = load_data()

    X, y, encoder = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = train_model(X_train, y_train)

    evaluate_model(model, X_test, y_test)

    save_model(model, encoder)


if __name__ == "__main__":
    main()