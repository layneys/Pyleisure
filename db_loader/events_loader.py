import time
from datetime import datetime, timedelta
import json
import  requests


def get_start_of_last_month_unix():
    now = datetime.now()
    current_date = datetime(now.year, now.month, now.day)
    start_of_last_month = current_date - timedelta(weeks=1)
    return int(time.mktime(start_of_last_month.timetuple()))


def get_weekly_data_by_city(city: str, page:int):
    actual_time = get_start_of_last_month_unix()
    url = f'https://kudago.com/public-api/v1.4/events/?lang=&fields=id,dates,title,slug,place,description,\
    body_text,categories,tagline,price,is_free,images,favorites_count,tags,site_url,participants&page={page}&actual_since={actual_time}'
    response = requests.get(url)
    data = response.json()
    return data


def fill_fake_db():

    i=1

    while True:
        data = get_weekly_data_by_city('msk', i)
        with open('db_loader/fake_db.json', 'a', encoding='utf-8') as f:
            json.dump(data["results"], f, ensure_ascii=False, indent=4)
        i+=1
        print(i)
        if data["next"] is None:
            break

if __name__ == "__main__":
    pass