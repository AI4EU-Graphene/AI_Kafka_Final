# smart-ml-forecaster/forecaster.py

import logging
import numpy as np

logger = logging.getLogger("Forecaster")

# List of features used during training — must match training pipeline
FEATURE_COLUMNS = [
    "demand", "demand_lag1", "demand_lag2",
    "demand_mean3", "demand_std3",
    "hour", "dayofweek"
]

def predict(model, features: dict) -> dict:
    try:
        X = np.array([[features[col] for col in FEATURE_COLUMNS]])
        forecast = model.predict(X)[0]

        return {
            "timestamp": features["timestamp"],
            "input_demand": features["demand"],
            "forecast_demand": forecast,
            "model_version": "v1"
        }

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return None