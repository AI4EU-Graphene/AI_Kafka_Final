# smart-ml-preprocessor/feature_engineer.py

import pandas as pd
import logging

logger = logging.getLogger("FeatureEngineer")

# We use a rolling window of past 3 points for features
class FeatureEngineer:
    def __init__(self):
        self.history = []

    def transform(self, record: dict) -> dict:
        self.history.append(record)
        if len(self.history) < 3:
            return None  # Not enough history yet

        # Keep only latest 3
        self.history = self.history[-3:]

        df = pd.DataFrame(self.history)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        # Basic features
        current = df.iloc[-1].copy()
        current["hour"] = current["timestamp"].hour
        current["dayofweek"] = current["timestamp"].dayofweek

        # Lag features
        current["demand_lag1"] = df.iloc[-2]["demand"]
        current["demand_lag2"] = df.iloc[-3]["demand"]

        # Rolling stats
        current["demand_mean3"] = df["demand"].rolling(3).mean().iloc[-1]
        current["demand_std3"] = df["demand"].rolling(3).std().iloc[-1]

        return current.to_dict()