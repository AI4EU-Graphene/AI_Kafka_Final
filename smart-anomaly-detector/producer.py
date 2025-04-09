# smart-ingestor/producer.py

from kafka import KafkaProducer
import json
import os
import logging

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaProducer")

def create_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5
        )
        logger.info(f"Connected to Kafka at {KAFKA_BROKER_URL}")
        return producer
    except Exception as e:
        logger.error(f"Kafka producer setup failed: {str(e)}")
        raise