# smart-alert-engine/alert_loop.py

import os
import logging
from consumer import create_consumer
from producer import create_producer
from alerter import generate_alert

INPUT_TOPIC = os.getenv("ANOMALY_TOPIC", "anomaly_output")
OUTPUT_TOPIC = os.getenv("ALERT_TOPIC", "alert_output")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AlertLoop")

def main():
    consumer = create_consumer(INPUT_TOPIC)
    producer = create_producer()

    logger.info(f"Listening to {INPUT_TOPIC} for alerts...")

    for message in consumer:
        record = message.value
        alert = generate_alert(record)

        if alert:
            producer.send(OUTPUT_TOPIC, value=alert)
            logger.info(f"Alert sent for {alert['timestamp']}")
        else:
            logger.info("No alert triggered for this record.")

if __name__ == "__main__":
    main()