# ai-pipeline/train_selector_model.py

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Simulated historical data
# You can later replace this with real logs from your system
data = [
    {"feature": "SYSTEM_DEMAND", "forecast": 6000, "region": "ALL", "sequence": ["ingestor", "preprocessor", "trainer", "ml_preprocessor", "forecaster"]},
    {"feature": "CO2_INTENSITY", "forecast": 180, "region": "ROI", "sequence": ["ingestor", "preprocessor", "ml_preprocessor", "forecaster"]},
    {"feature": "WIND_ACTUAL", "forecast": 300, "region": "NI", "sequence": ["ingestor", "preprocessor", "ml_preprocessor"]},
]

df = pd.DataFrame(data)
df["target"] = df["sequence"].apply(lambda seq: ",".join(seq))
df = df.drop(columns=["sequence"])

# Features
X = df.drop(columns=["target"])
X = pd.get_dummies(X)
y = df["target"]

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Save model and feature columns
joblib.dump({
    "model": clf,
    "features": list(X.columns)
}, "selector_model.pkl")

print("✅ selector_model.pkl saved")