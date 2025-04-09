# smart-storage-optimizer/optimize_loop.py

import os
import logging
from consumer import create_consumer
from optimizer_logic import optimize_storage

INPUT_TOPIC = os.getenv("OPTIMIZER_INPUT_TOPIC", "anomaly_output")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OptimizerLoop")

def main():
    consumer = create_consumer(INPUT_TOPIC)
    logger.info(f"Listening on topic '{INPUT_TOPIC}' for storage optimization triggers...")

    for message in consumer:
        record = message.value
        logger.info(f"Received record: {record}")

        if record.get("anomaly"):
            logger.info("Anomaly detected, running storage optimization.")
            optimize_storage(record)
        else:
            logger.info("No anomaly. Skipping optimization.")

if __name__ == "__main__":
    main()