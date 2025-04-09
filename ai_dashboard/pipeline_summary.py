# ai_dashboard/pipeline_summary.py

from collections import deque
from datetime import datetime

class PipelineSummary:
    def __init__(self, max_events=50000):
        self.forecast_events = deque(maxlen=max_events)
        self.anomalies = deque(maxlen=max_events)

    def add_forecast(self, data):
        print("📊 Forecast received in dashboard:", data)
        self.forecast_events.append((datetime.utcnow(), data))

    def add_anomaly(self, data):
        print("⚠️ Anomaly received in dashboard:", data)
        self.anomalies.append((datetime.utcnow(), data))

    def generate_summary(self):
        forecasts = [f[1] for f in self.forecast_events if 'forecast' in f[1]]
        anomalies = [f[1] for f in self.anomalies if f[1].get('anomaly')]

        summary = f"""
🔢 Pipeline Data Summary:

• Total forecasts: {len(forecasts)}
• Total anomalies flagged: {len(anomalies)}
"""

        if forecasts:
            values = [f['forecast'] for f in forecasts]
            avg = round(sum(values) / len(values), 2)
            min_val = round(min(values), 2)
            max_val = round(max(values), 2)
            summary += f"• Forecast average: {avg} MW (min: {min_val}, max: {max_val})\n"

            recent = forecasts[-5:]
            summary += "\n🕒 Recent Forecasts:\n"
            for f in recent:
                summary += f"- {f['timestamp']} → {f['forecast']} MW\n"

        if anomalies:
            summary += "\n⚠️ Latest Anomaly:\n"
            summary += f"{anomalies[-1]}\n"

        return summary.strip()