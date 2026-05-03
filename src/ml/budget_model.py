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


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


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

    encoder = OneHotEncoder(sparse_output=False)
    event_encoded = encoder.fit_transform(X[["event_type"]])

    event_df = pd.DataFrame(
        event_encoded, columns=encoder.get_feature_names_out(["event_type"])
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
# 🔥 NEW: MODEL LOADING + PREDICTION
# -------------------------------

def load_model():
    bundle = joblib.load(MODEL_PATH)
    return bundle["model"], bundle["encoder"]


def predict_budget(input_data: dict):
    model, encoder = load_model()

    df = pd.DataFrame([input_data])

    # Encode event_type
    event_encoded = encoder.transform(df[["event_type"]])
    event_df = pd.DataFrame(
        event_encoded,
        columns=encoder.get_feature_names_out(["event_type"]),
    )

    df = df.drop(columns=["event_type"]).reset_index(drop=True)
    df = pd.concat([df, event_df], axis=1)

    preds = model.predict(df)[0]

    # 🔥 IMPORTANT: Normalize predictions so sum = 1
    preds = preds / preds.sum()

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

    result = dict(zip(categories, preds))

    return result


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