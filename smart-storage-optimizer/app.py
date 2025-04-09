from flask import Flask, jsonify
from kafka import KafkaConsumer
import json
import threading
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-storage-optimizer")

KAFKA_TOPIC = "forecast_output"
KAFKA_SERVER = "kafka:9092"

def consume_and_optimize():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="smart-storage-optimizer-group"
    )

    for message in consumer:
        record = message.value
        logger.info("smart-storage-optimizer received: %s", record)

        forecast = record.get("forecast", 0)
        if forecast > 9000:
            logger.info("High forecast detected: Activating storage discharge")
        elif forecast < 2000:
            logger.info("Low forecast detected: Charging storage")

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "smart-storage-optimizer service running"})

if __name__ == "__main__":
    threading.Thread(target=consume_and_optimize, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)