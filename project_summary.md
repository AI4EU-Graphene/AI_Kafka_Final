
# 🔧 Smart Energy Pipeline Project Overview

This project is a distributed, event-driven energy analytics pipeline using **Kafka** and **Python microservices**. Below is a summary of the pipeline structure and how AI is intended to be integrated using **Ollama** on a MacBook Air M3.

---

## 📦 Service Nodes & Responsibilities

1. **smart-ingestor**  
   - Streams raw energy demand data.  
   - Kafka Topic: `raw_energy_data`

2. **smart-preprocessor**  
   - Cleans raw input data.  
   - Kafka Topic: `raw_energy_data` → `preprocessed_data`

3. **smart-ml-preprocessor**  
   - Generates features (lags, stats, time).  
   - Kafka Topic: `preprocessed_data` → `ml_ready_data`

4. **smart-model-trainer**  
   - Trains ML models by feature.  
   - Outputs: `model_<feature>.pkl` → `/models` directory

5. **smart-ml-forecaster**  
   - Uses trained models to predict demand.  
   - Kafka Topic: `ml_ready_data` → `forecast_output`

6. **smart-anomaly-detector**  
   - Flags deviations between forecast and actual.  
   - Kafka Topic: `forecast_output` → `anomaly_output`

7. **smart-alert-engine**  
   - Raises alerts based on anomalies.  
   - Kafka Topic: `anomaly_output` → `alert_output`

8. **smart-grid-rebalancer**  
   - Simulated rebalancer (to be implemented).

9. **smart-storage-optimizer**  
   - Placeholder for future storage optimization logic.

10. **ai-pipeline (Deprecated)**  
    - Originally for orchestration. Now, Kafka handles flow automatically.

---

## 🧠 AI Integration Vision (via Ollama)

### Purpose:
Use a **local LLM** (like `mistral` via **Ollama**) **not to run nodes**, but to provide intelligent observability, insights, and decision support.

### Key AI Functions:

- **🧭 Inference Advisor**  
  Understands pipeline state, suggests debugging or improvements.

- **📊 Visual Insight Generator**  
  Live graphs of forecast vs demand, anomaly frequency, etc.

- **🧠 Log/Topic Interpreter**  
  Parses Kafka logs/messages for anomalies, latency, drift.

- **🤖 Command-Line AI Buddy**  
  Ask: "Which nodes are lagging?" or "Top anomaly features today?"

---

## 🛠️ AI Setup Guide

- **System**: MacBook Air M3  
- **Install Ollama**: https://ollama.com  
- **Model Suggestion**: `mistral`, `llama2`  
- **Hook Options**:  
  - Kafka topic consumer  
  - Log file analyzer  
  - Flask `/health` endpoints  

- **Future Add-ons**:  
  - Web dashboard (Flask + Chart.js)  
  - Historical data summarization  
  - Alert visualization

---

This file helps onboard anyone (or future-you) to understand how the AI and pipeline work together without interfering with the core Kafka-driven automation.
