import os
import logging
from consumer import create_consumer
from trainer import train_model
from feature_engineer import FeatureEngineer

INPUT_TOPIC = os.getenv("TRAINING_TOPIC", "ml_ready_data")
BATCH_SIZE = int(os.getenv("TRAINING_BATCH_SIZE", 100000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ModelTrainer")

def stream_and_train():
    consumer = create_consumer(INPUT_TOPIC)
    engineer = FeatureEngineer()
    batches = {}

    logger.info(f"Listening to {INPUT_TOPIC} for training data...")

    for message in consumer:
        record = message.value
        logger.info(f"Received training record: {record}")

        record["demand"] = record.pop("value")
        feature_type = record["feature"]

        engineered = engineer.transform(record)
        if not engineered:
            continue

        # Group batches by feature
        if feature_type not in batches:
            batches[feature_type] = []

        batches[feature_type].append(engineered)

        if len(batches[feature_type]) >= BATCH_SIZE:
            model_path = f"/models/model_{feature_type}.pkl"

            if os.path.exists(model_path):
                logger.info(f"Model already exists for {feature_type}. Skipping training.")
            else:
                logger.info(f"Collected {BATCH_SIZE} samples for {feature_type}. Training model...")
                train_model(batches[feature_type], save_path=model_path)

            batches[feature_type].clear()