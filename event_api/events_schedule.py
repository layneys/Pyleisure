import schedule
import time
from events_loader import fill_fake_event_db

fill_fake_event_db()

def run_events_loader():
    schedule.every().day.at("00:01").do(fill_fake_event_db)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    fill_fake_event_db()
    run_events_loader()
