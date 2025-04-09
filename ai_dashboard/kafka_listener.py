# ai_dashboard/kafka_listener.py

import threading
import json
from kafka import KafkaConsumer
from pipeline_summary import PipelineSummary

summary = PipelineSummary()

def listen_to_topic(topic, handler):
    print(f"🔄 Starting listener for topic: {topic}")
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers='kafka:9092',  # Docker-mapped host access
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        for message in consumer:
            print(f"📩 Received on {topic}: {message.value}")
            handler(message.value)
    except Exception as e:
        print(f"❌ Failed to connect to Kafka topic '{topic}': {e}")

def start_kafka_listeners():
    threading.Thread(target=listen_to_topic, args=("forecast_output", summary.add_forecast), daemon=True).start()
    threading.Thread(target=listen_to_topic, args=("anomaly_output", summary.add_anomaly), daemon=True).start()