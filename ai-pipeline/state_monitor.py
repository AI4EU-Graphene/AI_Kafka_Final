import requests

SERVICES = {
    "trainer": "http://smart-model-trainer:5000/health",
    "preprocessor": "http://smart-preprocessor:5000/health",
    "ml_preprocessor": "http://smart-ml-preprocessor:5000/health",
    "forecaster": "http://smart-ml-forecaster:5000/health",
    "detector": "http://smart-anomaly-detector:5000/health",
    "alert": "http://smart-alert-engine:5000/health",
    "ingestor": "http://smart-ingestor:5000/health"
}

def get_pipeline_state():
    state = {}
    for name, url in SERVICES.items():
        try:
            resp = requests.get(url, timeout=2)
            state[name] = "ready" if resp.status_code == 200 else "unavailable"
        except:
            state[name] = "down"
    return state

def get_state():
    # Simulated static state (you can extend this later)
    return {
        "preprocessor": "ready",
        "trainer": "ready",
        "ml_preprocessor": "ready",
        "forecaster": "ready",
        "detector": "ready",
        "alert": "ready",
        "ingestor": "ready"
    }