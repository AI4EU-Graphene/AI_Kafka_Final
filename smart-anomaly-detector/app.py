from flask import Flask, jsonify
from kafka import KafkaConsumer, KafkaProducer
import json
import threading
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-anomaly-detector")

KAFKA_TOPIC_CONSUME = "forecast_output"
KAFKA_TOPIC_PRODUCE = "anomaly_output"
KAFKA_SERVER = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def detect_anomaly(record):
    # Naive rule-based anomaly detector
    forecast = record.get("forecast", 0)
    if forecast > 10000 or forecast < 1000:
        record["anomaly"] = True
    else:
        record["anomaly"] = False
    return record

def consume_and_detect():
    consumer = KafkaConsumer(
        KAFKA_TOPIC_CONSUME,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="smart-anomaly-detector-group"
    )

    for message in consumer:
        record = message.value
        logger.info("smart-anomaly-detector consumed: %s", record)

        result = detect_anomaly(record)
        producer.send(KAFKA_TOPIC_PRODUCE, value=result)
        logger.info("smart-anomaly-detector produced: %s", result)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "smart-anomaly-detector service running"})

if __name__ == "__main__":
    threading.Thread(target=consume_and_detect, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)