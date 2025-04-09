import asyncio
import os
import logging
from backoff import on_exception, expo
import httpx
import pandas as pd
from httpx import HTTPStatusError
from tqdm.asyncio import tqdm
from datetime import datetime
from kafka import KafkaProducer
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)

KAFKA_TOPIC = "raw_energy_data"
KAFKA_SERVER = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

@on_exception(expo, HTTPStatusError, max_tries=8)
async def fetch_data(client, api, timeout=25):
    try:
        response = await client.get(api, timeout=timeout)
        response.raise_for_status()
        return response.json()["Rows"]
    except HTTPStatusError as e:
        logging.error(f"HTTPStatusError for API {api}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error for API {api}: {e}")
        raise

async def get_historic_data(client, region="ALL", semaphore: asyncio.Semaphore = None):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    categories = ["demandactual", "generationactual", "windactual", "interconnection", "co2intensity", "co2emission", "SnspALL"]
    year_range = (24, 25)  # Only for 2024

    for category in tqdm(categories, desc=f"Fetching categories for {region}"):
        for year in range(*year_range):
            for month in months:
                month_idx = months.index(month)
                next_month = months[0] if month_idx == 11 else months[month_idx + 1]
                next_year = year + 1 if month_idx == 11 else year

                api = (
                    f"https://www.smartgriddashboard.com/DashboardService.svc/data?"
                    f"area={category}&region={region}&"
                    f"datefrom=01-{month}-20{year}+00%3A00&"
                    f"dateto=01-{next_month}-20{next_year}+21%3A59"
                )

                async with semaphore:
                    try:
                        data = await fetch_data(client, api)
                        for record in data:
                            producer.send(KAFKA_TOPIC, value=record)
                        logging.info(f"Streamed {len(data)} records from {api}")
                    except Exception as e:
                        logging.warning(f"Failed to fetch/process data for {api}: {e}")
                        continue
async def get_live_data(client, region="ALL", semaphore: asyncio.Semaphore = None):
    categories = ["demandactual", "generationactual", "windactual", "interconnection", "co2intensity", "co2emission", "SnspALL"]

    while True:
        current_date = datetime.now().strftime("%d-%b-%Y+%H%%3A%M")
        for category in categories:
            api = (
                f"https://www.smartgriddashboard.com/DashboardService.svc/data?"
                f"area={category}&region={region}&"
                f"datefrom={current_date}&dateto={current_date}"
            )
            async with semaphore:
                try:
                    data = await fetch_data(client, api)
                    for record in data:
                        producer.send(KAFKA_TOPIC, value=record)
                    logging.info(f"Streamed {len(data)} records from {api}")
                except Exception as e:
                    logging.warning(f"Live fetch failed for {api}: {e}")
        await asyncio.sleep(60)  # Poll every minute

async def main():
    async with httpx.AsyncClient(http2=True) as client:
        semaphore = asyncio.Semaphore(10)
        regions = ["ALL", "ROI", "NI"]
        tasks = [get_historic_data(client, region, semaphore) for region in regions]
        await asyncio.gather(*tasks)


def download_data_main():
    asyncio.run(main())
def run():
    download_data_main()