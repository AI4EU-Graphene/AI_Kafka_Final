from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from model_loader import predict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-ml-forecaster")

KAFKA_BROKER_URL = "kafka:9092"
INPUT_TOPIC = "ml_ready_data"
OUTPUT_TOPIC = "forecast_results"

def consume_and_forecast():
    consumer = KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="ml-forecaster-group",
        auto_offset_reset="earliest"
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    for message in consumer:
        data = message.value
        logger.info("smart-ml-forecaster consumed: %s", data)

        forecast = predict(data)
        if forecast is not None:
            data["forecast"] = forecast
            logger.info("smart-ml-forecaster produced: %s", data)
            producer.send(OUTPUT_TOPIC, value=data)