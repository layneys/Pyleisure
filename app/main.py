from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model.model import LLM_Get_Ans
from model.parser import format_data_for_llm
from app.dao import UsersDAO, EventsDAO, WeatherDAO, ChoicesDAO
#from app.bot import user_telegram_id
import logging
from app.bot import lifespan, bot, dp

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
    #print(user_telegram_id)
    #user_data = await UsersDAO.get_user_data(user_telegram_id)
    events_data = await EventsDAO.get_event_data()
    weather_data = await WeatherDAO.get_weather_data('Moscow')
    user, events, weather = format_data_for_llm(events_data, weather_data)
    #print(user_data)
    #print(user)
    mocked_prefs = '''
        {
            "preferred_activity": "active",
            "budget": "medium",
            "duration_hours": 3,
            "group_type": "friends",
            "additional_notes": "Prefer outdoor activities"
        }
        '''

    # model_response = await LLM_Get_Ans(prefs, events, weather, prompt)
    model_response = await LLM_Get_Ans(mocked_prefs, events, weather, prompt)
    print(type(weather_data))
    print(weather_data)
    print(model_response)
    return templates.TemplateResponse("event_list.html", {"request": request,
                                                           "events": events_data,
                                                           "weather": weather_data,
                                                          "model_response": model_response})


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = await request.json()
    await dp.feed_update(bot, update)
    logging.info("Update processed")

# Имитация текущего пользователя
def get_current_user_id():
    return 1  # Пример: текущий пользователь с id = 1

@app.post("/liked/{event_id}")
async def like_event(event_id: int):
    user_id = get_current_user_id()
    print(event_id)
    try:
        # Добавление записи о лайке в базу данных
        await ChoicesDAO.add(telegram_id=user_id, event_id=event_id)
        return {"message": f"Event {event_id} liked successfully"}
    except Exception as e:
        logging.error(f"Ошибка при добавлении лайка: {e}")
        return {"error": "Произошла ошибка"}

@app.get("/liked", response_class=HTMLResponse)
async def get_liked(request: Request):
    try:
        user_id = get_current_user_id()

        liked_events = ChoicesDAO.liked_events(user_id)
        return templates.TemplateResponse("liked_events.html", {
            "request": request,
            "events": liked_events
        })

    except Exception as e:
        print(e)
