import schedule
import time
from weather_loader import fill_weather_db
from app.dao import WeatherDAO
import asyncio

async def run():
    await WeatherDAO.delete_irrelevant_weather()
    await fill_weather_db()

def run_weather_loader():
    schedule.every().hour.at(":00").do(asyncio.run(run()))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    #fill_weather_db()
    run_weather_loader()