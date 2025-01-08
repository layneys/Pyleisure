from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model.model import LLM_Get_Ans
from model.parser import format_data_for_llm
from app.dao import EventsDAO, WeatherDAO, ChoicesDAO
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/list", response_class=HTMLResponse)
async def process_data(
    request: Request,
    choice: str = Form(...), prompt: str = Form(...)
    ):
    # events = await get_events_page(choice) get from database
    # weather = await get_weather(choice) get from database


    events_data = await EventsDAO.get_event_data()
    weather_data = await WeatherDAO.get_weather_data('Moscow')
    user_data, events, weather = format_data_for_llm(events_data, weather_data)

    mocked_prefs = '''
        {
            "preferred_activity": "active",
            "budget": "medium",
            "duration_hours": 3,
            "group_type": "friends",
            "additional_notes": "Prefer outdoor activities"
        }
        '''

    # mocked_events = '''
    # {
    #     "event_name": "Summer Jazz Festival",
    #     "location": "Central Park",
    #     "date": "2025-07-20",
    #     "time": "18:00",
    #     "price_usd": 50
    # }
    # '''
    # mocked_weather = '''
    # {
    #     "city": "New York",
    #     "temperature_celsius": 25,
    #     "weather_condition": "sunny",
    #     "humidity_percent": 60,
    #     "wind_speed_kmh": 15
    # }
    # '''

    # model_response = await LLM_Get_Ans(prefs, events, weather, prompt)
    model_response = await LLM_Get_Ans(mocked_prefs, events, weather, prompt)
    print(type(weather_data))
    print(weather_data)
    print(model_response)
    return templates.TemplateResponse("event_list.html", {"request": request,
                                                           "events": events_data,
                                                           "weather": weather_data,
                                                          "model_response": model_response})

@app.get("/liked", response_class=HTMLResponse)
async def get_liked(request: Request):

    liked_events = ChoicesDAO.liked_events(types.Message.from_user.id)

    return templates.TemplateResponse("liked_events.html", {
        "request": request,
        "events": liked_events
    })
