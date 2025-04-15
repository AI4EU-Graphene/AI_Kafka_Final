import asyncio
import os
import logging
from async_eirgrid_downloader import get_live_data
from httpx import AsyncClient
from kafka import KafkaProducer
import json

def create_producer():
    return KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_SERVER", "kafka:9092"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_energy_data")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartIngestor")

async def ingest_data():
    producer = create_producer()
    async with AsyncClient(http2=True) as client:
        semaphore = asyncio.Semaphore(10)
        while True:
            async for df in get_live_data(client, region="ALL", semaphore=semaphore):
                for _, row in df.iterrows():
                    message = row.to_dict()
                    producer.send(KAFKA_TOPIC, value=message)
                logger.info(f"Published {len(df)} live records to Kafka")
            await asyncio.sleep(10)  

if __name__ == "__main__":
    asyncio.run(ingest_data())