import json
import requests
import logging
from ai_selector import predict_sequence
from state_monitor import get_state  # optional state use

logger = logging.getLogger("DecisionEngine")

LOG_FILE = "pipeline_sequence_log.jsonl"

def handle_forecast(record):
    state = {
        "preprocessor": "ready",
        "trainer": "ready",
        "ml_preprocessor": "ready",
        "forecaster": "ready",
        "detector": "ready",
        "alert": "ready",
        "ingestor": "ready"
    }

    sequence = predict_sequence(state, record)
    logger.info(f"AI-decided pipeline sequence: {sequence}")

    # Log it for training
    log = {
        "feature": record.get("feature"),
        "forecast": record.get("forecast"),
        "sequence": sequence
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")

    for service in sequence:
        try:
            logger.info(f"Triggering {service}...")
            requests.post(f"http://smart-{service}:5000/trigger")
        except Exception as e:
            logger.error(f"Failed to trigger {service}: {e}")