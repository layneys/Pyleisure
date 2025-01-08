import os

from alembic.command import current
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
from app.models import Weather
from app.dao import WeatherDAO

load_dotenv()

api_key = 'your_key'

cities_names = {
    "msk": "Moscow",
    "spb": "Saint Petersburg",
    "ekb": "Ekaterinburg",
}

def get_weather(city: str):
    response_list = []
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={cities_names[city]}&aqi=no"'
    response = requests.get(url)
    response_json = response.json()
    return response_json


async def fill_weather_db():
    for city in ["msk", "spb", "ekb"]:
        data = get_weather(city)
        await WeatherDAO.add(city=data['location']['name'],
            date=datetime.strptime(data['location']['localtime'][:10], "%Y-%m-%d").date(),
            temperature=data['current']['temp_c'],
            description=data['current']['condition']['text'],)


if __name__ == "__main__":
    import asyncio


    async def run():
        await fill_weather_db()


    asyncio.run(run())