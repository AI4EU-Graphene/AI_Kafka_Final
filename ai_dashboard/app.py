from flask import Flask, render_template, request, jsonify
import requests
from kafka_listener import start_kafka_listeners, summary
from datetime import datetime

app = Flask(__name__)
OLLAMA_ENDPOINT = "http://host.docker.internal:11434/api/generate"

start_kafka_listeners()

@app.route("/", methods=["GET", "POST"])
def index():
    ai_response = ""
    if request.method == "POST":
        user_prompt = request.form["prompt"]
        context_prompt = summary.generate_summary()
        full_prompt = f"{context_prompt}\n\nUser Query: {user_prompt}"

        try:
            response = requests.post(
                OLLAMA_ENDPOINT,
                json={"model": "mistral", "prompt": full_prompt, "stream": False}
            )
            ai_response = response.json()["response"]
        except Exception as e:
            ai_response = f"❌ Error: {str(e)}"
    return render_template("index.html", ai_response=ai_response)

@app.route('/api/forecast-stats')
def forecast_stats():
    forecasts = [f[1] for f in summary.forecast_events if 'forecast' in f[1]]
    if not forecasts:
        return jsonify({'average': None, 'data': [], 'labels': []})

    values = [f['forecast'] for f in forecasts]
    times = [f['timestamp'][-5:] for f in forecasts]
    return jsonify({'average': round(sum(values)/len(values), 2), 'data': values, 'labels': times})

@app.route('/api/anomaly-trend')
def anomaly_trend():
    anomalies = [f[1] for f in summary.anomalies][-10:]
    timestamps = [a['timestamp'][-8:] for a in anomalies]
    values = [a['demand'] for a in anomalies]
    return jsonify({'labels': timestamps, 'data': values})

@app.route('/api/summary')
def get_summary():
    forecasts = [f[1] for f in summary.forecast_events]
    anomalies = [f[1] for f in summary.anomalies if f[1].get('anomaly')]
    return jsonify({
        'forecast_count': len(forecasts),
        'anomaly_count': len(anomalies)
    })

@app.route('/api/chart-data')
def chart_data():
    data = [f[1] for f in summary.forecast_events if 'forecast' in f[1]]

    if not data:
        return jsonify({'avg_forecast': 0, 'timestamps': [], 'forecasts': [], 'demands': [], 'lag1': [], 'lag2': [], 'means': [], 'std_low': [], 'std_high': []})

    timestamps = [d['timestamp'][-8:] for d in data]
    forecasts = [d['forecast'] for d in data]
    demands = [d['demand'] for d in data]
    lag1 = [d['demand_lag1'] for d in data]
    lag2 = [d['demand_lag2'] for d in data]
    mean3 = [d['demand_mean3'] for d in data]
    std3 = [d['demand_std3'] for d in data]

    std_low = [round(m - s, 2) for m, s in zip(mean3, std3)]
    std_high = [round(m + s, 2) for m, s in zip(mean3, std3)]

    avg = round(sum(forecasts) / len(forecasts), 2)

    return jsonify({
        'avg_forecast': avg,
        'timestamps': timestamps,
        'forecasts': forecasts,
        'demands': demands,
        'lag1': lag1,
        'lag2': lag2,
        'means': mean3,
        'std_low': std_low,
        'std_high': std_high
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
