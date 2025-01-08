import httpx
import time
from datetime import datetime, timedelta
from external.parser import parse_input

def get_start_of_today_unix():
    now = datetime.now()
    current_day = datetime(now.year, now.month, now.day)-timedelta(days=1)
    return int(time.mktime(current_day.timetuple()))


async def get_events_page(city: str, retries = 10):
    attempt = 0
    while attempt < retries:
        try:
            async with httpx.AsyncClient() as client:

                actual_time = get_start_of_today_unix()
                url = f'https://kudago.com/public-api/v1.4/events/?lang=&fields=id,dates,title,slug,place,description,body_text,categories,tagline,price,is_free,images,favorites_count,tags,site_url,participants&actual_since={actual_time}&location={city}&expand=place'

                response = await client.get(url)
                data = response.json()

                for event in data["results"]:

                    if event["place"] is not None:

                        place_dict = {"title": event["place"]["title"],
                                      "address": event["place"]["address"]}

                        event["place"] = place_dict

                    event["parsed_description"] = parse_input(event["description"])
                    event["parsed_body_text"] = parse_input(event["body_text"])

                    if len(event["dates"]) > 1:
                        event["dates"] = event["dates"][-1]

                    if len(event["images"]) > 1:
                        event["images"] = event["images"][0]
            return data

        except httpx.ReadTimeout as e:
            attempt += 1
            if attempt < retries:
                time.sleep(1)
            else:
                raise e

if __name__ == "__main__":
    pass