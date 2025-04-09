import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GridRebalancer")

def rebalance_grid(anomaly_record):
    """
    Takes in an anomaly record and performs simulated grid rebalancing
    based on region and deviation.
    """
    timestamp = anomaly_record.get("timestamp")
    deviation = anomaly_record.get("deviation", 0)
    anomaly = anomaly_record.get("anomaly", False)

    if not anomaly:
        logger.info(f"No anomaly detected at {timestamp}. No action required.")
        return

    logger.info(f"⚠️ Rebalancing required at {timestamp}. Deviation: {deviation:.2%}")
    
    # Simulated logic: higher deviation = longer action time
    sleep_time = min(max(deviation * 10, 1), 5)  # between 1–5 seconds
    time.sleep(sleep_time)

    logger.info(f"✅ Grid rebalancing complete for {timestamp}")