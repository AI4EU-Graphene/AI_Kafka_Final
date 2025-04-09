import joblib
import logging

logger = logging.getLogger("AISelector")

SERVICES = [
    "preprocessor", "trainer", "ml_preprocessor",
    "forecaster", "detector", "alert", "ingestor"
]

model_bundle = joblib.load("selector_model.pkl")

def predict_sequence(state, forecast_record):
    feature = forecast_record.get("feature", "")
    forecast = forecast_record.get("forecast", 0)

    X = [[
        model_bundle["label_encoder"].transform([feature])[0],
        float(forecast)
    ]]
    preds = model_bundle["model"].predict(X)[0]

    return [
        svc for svc, include in zip(model_bundle["mlb"].classes_, preds) if include
    ]