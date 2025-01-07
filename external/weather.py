import os
from dotenv import load_dotenv
import httpx
load_dotenv()

api_key = os.getenv('WEATHER_API_KEY')

CITIES_NAMES = {
    "msk": "Moscow",
    "spb": "Saint Petersburg",
    "ekb": "Ekaterinburg",
}

async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={CITIES_NAMES[city]}&aqi=no")
        response_json = response.json()
    return response_json


if __name__ == '__main__':
    pass