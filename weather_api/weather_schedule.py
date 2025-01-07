'''import schedule
import time
from weather_api.weather_loader import fill_weather_db

def run_weather_loader():
    schedule.every().hour.at(":00").do(fill_weather_db)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    fill_weather_db()
    run_weather_loader()'''

import asyncio
import schedule
import time
from weather_api.weather_loader import fill_weather_db
from app.database import get_session

async def run_fill_weather_db():
    """Асинхронный метод для обновления данных погоды в базе."""
    async for session in get_session():
        await fill_weather_db(session)

def schedule_coroutine(coroutine):
    """Обёртка для запуска асинхронных задач в планировщике."""
    asyncio.run(coroutine())

def run_weather_scheduler():
    """Функция для запуска планировщика задач."""
    # Планировщик будет вызывать асинхронную функцию через обёртку
    schedule.every().hour.at(":00").do(schedule_coroutine, run_fill_weather_db)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Запуск однократного обновления перед запуском планировщика
    asyncio.run(run_fill_weather_db())
    run_weather_scheduler()

