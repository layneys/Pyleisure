import schedule
import time
from weather_api.weather_loader import fill_fake_weather_db

def run_weather_loader():
    schedule.every().hour.at(":00").do(fill_fake_weather_db)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    fill_fake_weather_db()
    run_weather_loader()