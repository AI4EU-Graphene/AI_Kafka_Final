# smart-alert-engine/alerter.py

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AlertEngine")

def generate_alert(record: dict) -> dict:
    """
    Generate alert if anomaly is True.
    """
    if not record.get("anomaly", False):
        return None

    alert = {
        "timestamp": record["timestamp"],
        "message": f"⚠️ Anomaly detected at {record['timestamp']}. Deviation: {record['deviation']:.2%}",
        "source": "smart-alert-engine",
        "severity": "HIGH"
    }

    logger.warning(alert["message"])
    return alert