import pandas as pd
import joblib
import os
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Trainer")

FEATURE_COLUMNS = [
    "demand", "demand_lag1", "demand_lag2",
    "demand_mean3", "demand_std3",
    "hour", "dayofweek"
]

TARGET_COLUMN = "demand"

def train_model(data: list, save_path: str = "models/latest_model.pkl"):
    df = pd.DataFrame(data)

    # Drop rows with missing values
    df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])

    if len(df) < 100:
        logger.warning("Not enough data to train.")
        return None

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    logger.info(f"Model trained. R^2 score: {score:.4f}")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model, save_path)
    logger.info(f"Model saved to {save_path}")
    return score