from flask import Flask, jsonify, request
import logging
from kafka import KafkaConsumer
import threading
import json
import time
time.sleep(30)
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-alert-engine")

KAFKA_TOPIC = "anomaly_results"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"

def consume_data():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="alert-engine-group"
    )
    for message in consumer:
        data = message.value
        logger.info("smart-alert-engine consumed: %s", data)

        if data.get("anomaly"):
            # Simulate alert action
            logger.warning("ALERT TRIGGERED: %s", data)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "smart-alert-engine service running"})

@app.route("/process", methods=["POST"])
def process_data():
    data = request.json
    logger.info("smart-alert-engine received data: %s", data)
    return jsonify({"status": "processed", "node": "smart-alert-engine"})

if __name__ == "__main__":
    threading.Thread(target=consume_data, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)