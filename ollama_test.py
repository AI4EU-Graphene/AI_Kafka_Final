import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "mistral", "prompt": "What does the smart-anomaly-detector do?", "stream": False}
)

print("AI says:", response.json()['response'])