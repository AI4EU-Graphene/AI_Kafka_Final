# smart-grid-rebalancer/rebalance_loop.py

import os
import logging
import time
from consumer import create_consumer
from rebalance_logic import rebalance_grid

INPUT_TOPIC = os.getenv("REBALANCE_INPUT_TOPIC", "anomaly_output")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RebalanceLoop")

def main():
    consumer = create_consumer(INPUT_TOPIC)
    logger.info(f"Listening on topic '{INPUT_TOPIC}' for grid rebalance triggers...")

    for message in consumer:
        record = message.value
        logger.info(f"Received record: {record}")

        if record.get("anomaly"):  # Basic trigger condition
            logger.info("Anomaly detected, triggering grid rebalancer.")
            rebalance_grid()
        else:
            logger.info("No anomaly. Skipping rebalancing.")

if __name__ == "__main__":
    main()