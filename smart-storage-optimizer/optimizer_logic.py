# smart-storage-optimizer/optimizer_logic.py

import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StorageOptimizer")

def optimize_storage(record):
    logger.info("Starting storage optimization analysis...")

    forecast = float(record.get("forecast_demand", 0.0))
    actual = float(record.get("input_demand", 0.0))

    action = "store" if forecast > actual else "release"

    time.sleep(2)  # simulate time delay
    logger.info(f"Storage optimization action: {action.upper()} — (forecast: {forecast}, actual: {actual})")

    return {
        "timestamp": record.get("timestamp"),
        "forecast": forecast,
        "actual": actual,
        "action": action
    }