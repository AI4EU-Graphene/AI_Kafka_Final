from flask import Flask, jsonify
from kafka import KafkaConsumer, KafkaProducer
import json
import threading
import logging
import time
from cleaner import clean_record

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-preprocessor")

KAFKA_TOPIC_CONSUME = "raw_energy_data"
KAFKA_TOPIC_PRODUCE = "preprocessed_data"
KAFKA_SERVER = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def consume_from_kafka():
    consumer = KafkaConsumer(
        KAFKA_TOPIC_CONSUME,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="smart-preprocessor-group"
    )
    for message in consumer:
        data = message.value
        logger.info("Preprocessing data: %s", data)

        cleaned = clean_record(data)
        logger.info("Cleaned: %s", cleaned)

        if cleaned:
            producer.send(KAFKA_TOPIC_PRODUCE, value=cleaned)
            logger.info("Published cleaned record to %s", KAFKA_TOPIC_PRODUCE)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "smart-preprocessor service running"})

if __name__ == "__main__":
    threading.Thread(target=consume_from_kafka, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
