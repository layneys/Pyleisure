import schedule
import time
import asyncio
from events_loader import fill_event_db
from app.dao import EventsDAO


async def run():
    await EventsDAO.delete_irrelevant_events()
    await fill_event_db()

def run_events_loader():
    schedule.every().day.at("00:01").do(asyncio.run(run()))
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    #fill_event_db()
    run_events_loader()
