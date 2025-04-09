# smart-ingestor/app.py

from flask import Flask, jsonify, request
import logging
from eirgrid_streamer import download_data_main  # streaming logic

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-ingestor")

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "smart-ingestor service running"})

@app.route("/stream", methods=["GET"])
def stream_data():
    logger.info("Streaming process started via /stream endpoint")
    try:
        download_data_main()
        return jsonify({"status": "Streaming started"})
    except Exception as e:
        logger.error(f"Streaming failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)