import joblib
import os
import logging

logger = logging.getLogger("ModelLoader")

MODEL_CACHE = {}

def load_model(feature):
    if feature in MODEL_CACHE:
        return MODEL_CACHE[feature]

    model_path = f"/models/model_{feature}.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        MODEL_CACHE[feature] = model
        return model
    else:
        logger.warning("Model for feature %s not found.", feature)
        return None

def predict(data):
    feature = data.get("feature")
    model = load_model(feature)
    if not model:
        return None

    try:
        input_vector = [[
            data.get("value", 0),
            data.get("demand_lag1", 0),
            data.get("demand_lag2", 0),
            data.get("demand_mean3", 0),
            data.get("demand_std3", 0),
            data.get("hour", 0),
            data.get("dayofweek", 0)
        ]]
        return model.predict(input_vector)[0]
    except Exception as e:
        logger.error("Prediction error: %s", e)
        return None