# smart-preprocessor/preprocessor.py

import os
import logging
from producer import create_producer
from consumer import create_consumer
from cleaner import clean_record

RAW_TOPIC = os.getenv("RAW_TOPIC", "raw_energy_data")
CLEANED_TOPIC = os.getenv("CLEANED_TOPIC", "preprocessed_data")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartPreprocessor")

def main():
    consumer = create_consumer(RAW_TOPIC)
    producer = create_producer()

    logger.info(f"Listening to topic: {RAW_TOPIC}")

    for message in consumer:
        record = message.value
        cleaned = clean_record(record)

        if cleaned:
            producer.send(CLEANED_TOPIC, value=cleaned)
            logger.info(f"Published cleaned record to {CLEANED_TOPIC}")
        else:
            logger.warning("Skipped uncleanable record")

if __name__ == "__main__":
    main()