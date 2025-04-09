
# ⚡ Smart AI Energy Dashboard

A real-time Kafka-powered AI pipeline for forecasting electricity demand, anomaly detection, and interactive analysis using an LLM. Inspired by EirGrid’s Smart Grid Dashboard.

---

## 🚀 Features

- 🔄 Real-time Kafka pipeline
- 🤖 ML forecaster using Random Forest (with demand lag & rolling stats)
- 📊 Beautiful Flask dashboard inspired by EirGrid
- 💬 AI assistant (via Ollama + Mistral) for natural language interaction
- 📈 Three dynamic charts: Forecast vs Demand, Lag Trends, Std Dev Band
- 🧠 Embedded summarization engine
- 🎨 Responsive UI using Chart.js & grid layout

---

## 🧱 Architecture

```plaintext
Kafka Topics ─► ML Forecaster ─► Dashboard + AI
               ▲                ▲
               └── Anomaly Check│
```

- **Kafka Topics**: `forecast_output`, `anomaly_output`
- **Forecaster**: Consumes raw demand data, predicts next step, flags anomalies
- **Dashboard**: Consumes, stores, visualizes and interfaces with AI
- **LLM**: Mistral via Ollama (local, streaming off)

---

## 🧰 Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-green)
![Kafka](https://img.shields.io/badge/Kafka-Streaming-orange)
![Ollama](https://img.shields.io/badge/Ollama-Mistral-brightgreen)
![Chart.js](https://img.shields.io/badge/Charts-Chart.js-purple)
![Docker](https://img.shields.io/badge/Container-Docker-blue)

---

## 🐳 How to Run

### 1. Clone this repo

```bash
git clone git@github.com:AI4EU-Graphene/AI_Kafka_Final.git
cd AI_Kafka_Final
```

### 2. Build & Start Docker

```bash
docker compose up --build
```

> This spins up Kafka, Zookeeper, the forecaster, and the AI dashboard.

### 3. Launch Ollama separately (if not in Docker)

```bash
ollama run mistral
```

Or preload model:

```bash
ollama pull mistral
```

---

## 📂 Folder Structure

```
.
├── app.py                    # Flask dashboard backend
├── templates/index.html      # Main UI (Smart Grid Inspired)
├── kafka_listener.py         # Kafka topic consumers
├── pipeline_summary.py       # In-memory state + summarizer
├── Dockerfile                # Forecaster container
├── docker-compose.yml        # Orchestration of all components
├── requirements.txt
└── README.md
```

---

## 🧠 Example AI Prompt

> "What is the current trend in demand anomalies for NI?"

AI will reply with stats, trend summaries, and flagged events using the latest Kafka stream data.

---

## 📸 UI Preview

> Insert screenshots of the dashboard for Forecast, Lag, and Std Dev charts here.

---

## 📜 License

MIT – use, fork, build cool stuff.

---

## 👨‍💻 Author

Made with ❤️ by [your-name] for AI4EU Graphene.
