# smart-ml-preprocessor/ml_preprocessor.py

from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from feature_engineer import FeatureEngineer

logger = logging.getLogger("smart-ml-preprocessor")

KAFKA_TOPIC = "preprocessed_data"
KAFKA_OUT_TOPIC = "ml_ready_data"
KAFKA_SERVER = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

engineer = FeatureEngineer()

def process_stream():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="ml-preprocessor-group"
    )

    for message in consumer:
        record = message.value
        logger.info(f"smart-ml-preprocessor consumed: {record}")

        enriched = engineer.transform(record)
        if enriched:
            enriched["processed_by"] = "ml-preprocessor"
            producer.send(KAFKA_OUT_TOPIC, value=enriched)
            logger.info(f"smart-ml-preprocessor produced: {enriched}")