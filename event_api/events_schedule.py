import schedule
import time
import asyncio
from event_api.events_loader import fill_event_db


fill_event_db()

def run_events_loader():
    schedule.every().day.at("00:01").do(fill_event_db)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    asyncio.run(fill_event_db())
    run_events_loader()
