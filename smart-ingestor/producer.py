# smart-ingestor/ingestor.py

import asyncio
import os
import logging
from producer import create_producer
from async_eirgrid_downloader import get_live_data

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_energy_data")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartIngestor")

async def ingest_data():
    from httpx import AsyncClient
    producer = create_producer()

    async with AsyncClient(http2=True) as client:
        semaphore = asyncio.Semaphore(10)
        async for df in get_live_data(client, region="ALL", semaphore=semaphore):
            for _, row in df.iterrows():
                message = row.to_dict()
                producer.send(KAFKA_TOPIC, value=message)
            logger.info(f"Published {len(df)} live records to Kafka")

if __name__ == "__main__":
    asyncio.run(ingest_data())