# smart-ml-preprocessor/consumer.py

from kafka import KafkaConsumer
import json
import os
import logging

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "smart-preprocessor-group")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaConsumer")

def create_consumer(topic):
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BROKER_URL,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=KAFKA_GROUP_ID,
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )
        logger.info(f"Connected to Kafka topic: {topic}")
        return consumer
    except Exception as e:
        logger.error(f"Kafka consumer setup failed: {str(e)}")
        raise