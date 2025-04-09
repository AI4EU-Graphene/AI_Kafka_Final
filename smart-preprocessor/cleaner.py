# smart-preprocessor/cleaner.py

import pandas as pd
import logging

# Force log level in case it's not inherited
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Cleaner")

def clean_record(record: dict) -> dict:
    try:
        logger.info(f"Attempting to clean record: {record}")

        # Handle missing timestamp
        if "EffectiveTime" in record:
            record["timestamp"] = pd.to_datetime(record["EffectiveTime"]).isoformat()
        else:
            logger.warning("Missing EffectiveTime in record.")
            return None

        # Validate required fields
        if not all(k in record for k in ("FieldName", "Region", "Value")):
            logger.warning(f"Missing fields in record: {record}")
            return None

        # Normalize the Value field
        try:
            if record["Value"] is None:
                logger.warning(f"Null Value found: {record}")
                return None
            record["Value"] = float(record["Value"])
            if record["Value"] < 0:
                record["Value"] = 0.0
        except Exception:
            logger.warning(f"Invalid Value in record: {record}")
            return None

        cleaned = {
            "timestamp": record["timestamp"],
            "feature": record["FieldName"],
            "region": record["Region"],
            "value": record["Value"]
        }

        logger.info(f"Cleaned result: {cleaned}")
        return cleaned

    except Exception as e:
        logger.warning(f"Failed to clean record: {e}")
        return None