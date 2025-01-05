import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

api_key = os.getenv('API_KEY')

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


def fill_fake_weather_db():

    db_path = os.path.abspath("./fake_weather_db.json")
    response_list = []
    for city in cities_names.keys():
        response_list.append(get_weather(city))
    with open(f'{db_path}', 'a', encoding='utf-8') as f:
        json.dump(response_list, f, ensure_ascii=False, indent=4)
    print(response_list)
    print('got weather!')

if __name__ == "__main__":
    pass


