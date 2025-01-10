from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model.model import LLM_Get_Ans
from model.parser import format_data_for_llm
from app.dao import UsersDAO, EventsDAO, WeatherDAO, ChoicesDAO
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, user_id: int = 0):
    username = UsersDAO.get_username_by_user_id(user_id)
    return templates.TemplateResponse("index.html", {"request": request, "username": username})


@app.post("/list", response_class=HTMLResponse)
async def process_data(
    request: Request,
    user_id: int = Query(default=0),
    choice: str = Form(...), prompt: str = Form(...)
    ):

    cities = {'Москва': 'Moscow', 'Санкт-Петербург': 'Saint Petersburg', 'Екатеринбург': 'Ekaterinburg'}

    user_data = await UsersDAO.get_user_data(user_id)
    city = cities[user_data['city']]
    print(type(city))
    print(city)
    events_data = await EventsDAO.get_event_data(city)
    weather_data = await WeatherDAO.get_weather_data(city)
    user, events, weather = format_data_for_llm(user_data, events_data, weather_data)
    # model_response = await LLM_Get_Ans(prefs, events, weather, prompt)
    model_response = await LLM_Get_Ans(user, events, weather, prompt)
    return templates.TemplateResponse("event_list.html", {"request": request,
                                                           "events": events_data,
                                                           "city": city,
                                                           "weather": weather_data,
                                                          "model_response": model_response})


@app.post("/liked/{event_id}")
@app.delete("/liked/{event_id}")
async def like_event(request: Request, event_id: int, user_id: int = Query(default=0)):
    method = request.method
    try:
        if method == "POST":
            # Добавление записи о лайке в базу данных
            res = await ChoicesDAO.find_one_or_none(telegram_id=user_id, event_id=event_id)
            if res != None:
                await ChoicesDAO.delete_event(telegram_id=user_id, event_id=event_id)
                return {"message": f"Event {event_id} deleted successfully"}
            else:
                await ChoicesDAO.add(telegram_id=user_id, event_id=event_id)
                return {"message": f"Event {event_id} liked successfully"}
        elif method == "DELETE":
            # Удаление записи о лайке из базы данных
            await ChoicesDAO.delete_event(telegram_id=user_id, event_id=event_id)
            return {"message": f"Event {event_id} deleted successfully"}
    except Exception as e:
        logging.error(f"Ошибка при добавлении/удалении лайка: {e}")
        return {"error": "Произошла ошибка"}


@app.get("/liked", response_class=JSONResponse)
async def get_liked(user_id: int = Query(default=0)):
    try:
        # Получение лайкнутых мероприятий из базы данных
        liked_events = await ChoicesDAO.liked_events(user_id)
        print(liked_events)

        return JSONResponse(content=liked_events)

    except Exception as e:
        logging.error(f"Ошибка при получении лайкнутых мероприятий: {e}")
        return JSONResponse(content={"error": "Произошла ошибка"}, status_code=500)