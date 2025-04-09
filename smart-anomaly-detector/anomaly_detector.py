# smart-anomaly-detector/anomaly_detector.py

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AnomalyDetector")

def detect_anomaly(record: dict, threshold=0.15) -> dict:
    """
    Compares input vs forecast demand. Flags if deviation > threshold.
    """
    actual = float(record.get("input_demand", 0.0))
    forecast = float(record.get("forecast_demand", 0.0))

    if actual == 0:
        return None  # skip invalid input

    deviation = abs(actual - forecast) / actual

    anomaly = deviation > threshold

    result = {
        "timestamp": record["timestamp"],
        "input_demand": actual,
        "forecast_demand": forecast,
        "deviation": deviation,
        "anomaly": anomaly,
        "threshold": threshold
    }

    if anomaly:
        logger.warning(f"Anomaly detected at {record['timestamp']} — Deviation: {deviation:.2f}")

    return result