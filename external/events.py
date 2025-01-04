import httpx
import time
from datetime import datetime, timedelta

def get_start_of_last_month_unix():
    now = datetime.now()
    current_date = datetime(now.year, now.month, now.day)
    start_of_last_month = current_date - timedelta(weeks=1)
    return int(time.mktime(start_of_last_month.timetuple()))


async def get_events_page(city: str):

    actual_time = get_start_of_last_month_unix()

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://kudago.com/public-api/v1.4/events/?lang=ru&actual_since={actual_time}&location={city}")
        response_json = response.json()
    return response_json


async def get_event_detail(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://kudago.com/public-api/v1.4/events/{id}/?lang=ru")
        response_json = response.json()
    return response_json

if __name__ == "__main__":
    pass