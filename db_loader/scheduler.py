import schedule
import time
from db_loader.events_loader import fill_fake_db

schedule.every().monday.at("00:00").do(fill_fake_db())  # Выполняется каждый понедельник

def run_loader():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    pass