import time
from dataclasses import replace
from datetime import datetime, timedelta
import requests
from lxml.builder import unicode
from sqlalchemy import union

from app.dao import EventsDAO
from external.events import parse_input

cities_names = {
    "msk": "Moscow",
    "spb": "Saint Petersburg",
    "ekb": "Ekaterinburg",
}

def get_start_of_today_unix():
    now = datetime.now()
    current_day = datetime(now.year, now.month, now.day) - timedelta(days=1)
    return int(time.mktime(current_day.timetuple()))


def get_weekly_data_by_city(city: str, page:int):
    actual_time = get_start_of_today_unix()
    url = f'https://kudago.com/public-api/v1.4/events/?lang=&fields=id,dates,title,slug,place,description,body_text,categories,tagline,price,is_free,images,favorites_count,tags,site_url,participants&page={page}&actual_since={actual_time}&location={city}&expand=place'
    response = requests.get(url)
    data = response.json()

    for event in data["results"]:
        event["parsed_description"] = parse_input(event["description"])
        event["parsed_body_text"] = parse_input(event["body_text"])


        if event["place"] is not None:

            place_dict = {"title": event["place"]["title"],
                     "address": event["place"]["address"]}

            event["place"] = place_dict

        if len(event["dates"]) > 1:
            event["dates"]=event["dates"][-1]

        if len(event["images"]) > 1:
            event["images"]=event["images"][0]

    return data


async def fill_event_db():
    for city in ["msk", "spb", "ekb"]:
        i = 1
        while True:
            data = get_weekly_data_by_city(city, i)
            for event_data in data["results"]:
                try:
                    await EventsDAO.add(event_id=event_data["id"],
                        event_title=event_data['title'],
                        event_city=cities_names[city],
                        event_place=event_data['place']['title'] + ', ' + event_data['place']['address'],
                        event_start_date=datetime.utcfromtimestamp(event_data.get("dates")['start']).strftime('%Y-%m-%d %H:%M:%S'),
                        event_end_date=datetime.utcfromtimestamp(event_data.get("dates")['end']).strftime('%Y-%m-%d %H:%M:%S'),
                        event_type=event_data.get("categories")[0],
                        event_description=event_data["description"],
                        event_price= 'Бесплатно' if event_data["price"] == "" else event_data["price"].replace('₽', 'руб.'),
                        event_img=event_data.get("images")[0]['image'],
                        event_url=event_data['site_url'],
                        event_favorites_count=event_data['favorites_count'])
                except:
                    pass

            i += 1
            print(f"i={i} for {city}")
            if data["next"] is None or i == 2:
                print(f'Finish events for {city}!')
                break

if __name__ == "__main__":
    pass
    # import asyncio
    #
    # async def run():
    #     await fill_event_db()
    #
    # asyncio.run(run())
