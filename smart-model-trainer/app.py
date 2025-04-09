from flask import Flask, jsonify
import logging
import threading
import time
from model_trainer import stream_and_train


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-model-trainer")

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "smart-model-trainer service running"})

if __name__ == "__main__":
    threading.Thread(target=stream_and_train, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)