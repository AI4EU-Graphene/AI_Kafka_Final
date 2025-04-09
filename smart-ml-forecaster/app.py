# smart-ml-forecaster/app.py

from flask import Flask, jsonify
from kafka import KafkaConsumer, KafkaProducer
import json
import threading
import logging
from model_loader import predict

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-ml-forecaster")

KAFKA_TOPIC_CONSUME = "ml_ready_data"
KAFKA_TOPIC_PRODUCE = "forecast_output"
KAFKA_SERVER = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def consume_and_forecast():
    consumer = KafkaConsumer(
        KAFKA_TOPIC_CONSUME,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="smart-ml-forecaster-group"
    )

    for message in consumer:
        record = message.value
        logger.info("smart-ml-forecaster consumed: %s", record)

        forecast = predict(record)
        if forecast is not None:
            record["forecast"] = forecast
            logger.info("smart-ml-forecaster produced: %s", record)
            producer.send(KAFKA_TOPIC_PRODUCE, value=record)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "smart-ml-forecaster service running"})

if __name__ == "__main__":
    threading.Thread(target=consume_and_forecast, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)