import time
from datetime import datetime, timedelta
import json
import  requests
import os

def get_start_of_today_unix():
    now = datetime.now()
    current_day = datetime(now.year, now.month, now.day)-timedelta(days=1)
    return int(time.mktime(current_day.timetuple()))


def get_weekly_data_by_city(city: str, page:int):
    actual_time = get_start_of_today_unix()
    url = f'https://kudago.com/public-api/v1.4/events/?lang=&fields=id,dates,title,slug,place,description,\
    body_text,categories,tagline,price,is_free,images,favorites_count,tags,site_url,participants&page={page}&actual_since={actual_time}&location={city}'
    response = requests.get(url)
    data = response.json()
    for event in data["results"]:
        if len(event["dates"]) > 1:
            event["dates"]=event["dates"][-1]
        if len(event["images"]) > 1:
            event["images"]=event["images"][0]
    return data


def fill_fake_event_db():

    db_path = os.path.abspath("./fake_event_db.json")

    for city in ["msk", "spb", "ekb"]:
        i = 1
        while True:
            data = get_weekly_data_by_city(city, i)
            with open(f'{db_path}', 'a', encoding='utf-8') as f:
                json.dump(data["results"], f, ensure_ascii=False, indent=4)
            i+=1
            print(f"i={i} for {city}")
            if (data["next"] is None) or i==2: #для экономии времени
                print(f'Finish events! for {city}')
                break

if __name__ == "__main__":
    pass