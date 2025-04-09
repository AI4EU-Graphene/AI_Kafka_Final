# smart-anomaly-detector/detector_loop.py

import os
import logging
from consumer import create_consumer
from producer import create_producer
from anomaly_detector import detect_anomaly

INPUT_TOPIC = os.getenv("FORECAST_TOPIC", "forecast_output")
OUTPUT_TOPIC = os.getenv("ANOMALY_TOPIC", "anomaly_output")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AnomalyDetectorLoop")

def main():
    consumer = create_consumer(INPUT_TOPIC)
    producer = create_producer()

    logger.info(f"Listening to {INPUT_TOPIC} for anomaly detection...")

    for message in consumer:
        record = message.value
        result = detect_anomaly(record)

        if result:
            producer.send(OUTPUT_TOPIC, value=result)
            logger.info(f"Published anomaly result for {result['timestamp']}")
        else:
            logger.warning("Skipping invalid or incomplete record.")

if __name__ == "__main__":
    main()