from flask import Flask
from kafka import KafkaConsumer
import json
import threading
import decision_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI-Pipeline")

KAFKA_BROKER_URL = "kafka:9092"
KAFKA_TOPIC = "forecast_results"

app = Flask(__name__)

def consume_forecasts():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="ai-pipeline-group",
        auto_offset_reset="earliest"
    )

    for message in consumer:
        record = message.value
        logger.info(f"Received forecast record: {record}")
        try:
            decision_engine.handle_forecast(record)
        except Exception as e:
            logger.error(f"Error processing record: {e}")

@app.route("/")
def health():
    return {"status": "ai-pipeline running"}

if __name__ == "__main__":
    threading.Thread(target=consume_forecasts, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)