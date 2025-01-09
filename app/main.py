from fastapi import FastAPI, Request, Form
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
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/list", response_class=HTMLResponse)
async def process_data(
    request: Request,
    choice: str = Form(...), prompt: str = Form(...)
    ):
    # events = await get_events_page(choice) get from database
    # weather = await get_weather(choice) get from database
    #print(user_telegram_id)
    user_data = await UsersDAO.get_user_data(user_id)
    print(user_id)
    print(user_data)
    events_data = await EventsDAO.get_event_data()
    weather_data = await WeatherDAO.get_weather_data('Moscow')
    user, events, weather = format_data_for_llm(user_data, events_data, weather_data)
    city = 'Moscow'
    #print(user_data)
    print(user)
    # mocked_prefs = '''
    #     {
    #         "preferred_activity": "active",
    #         "budget": "medium",
    #         "duration_hours": 3,
    #         "group_type": "friends",
    #         "additional_notes": "Prefer outdoor activities"
    #     }
    #     '''

    # model_response = await LLM_Get_Ans(prefs, events, weather, prompt)
    model_response = await LLM_Get_Ans(user, events, weather, prompt)
    print(type(weather_data))
    print(weather_data)
    print(model_response)
    return templates.TemplateResponse("event_list.html", {"request": request,
                                                           "events": events_data,
                                                           "city": city,
                                                           "weather": weather_data,
                                                          "model_response": model_response})


# Имитация текущего пользователя
def get_current_user_id():
    return 1  # Пример: текущий пользователь с id = 1

@app.post("/liked/{event_id}")
@app.delete("/liked/{event_id}")
async def like_event(request: Request, event_id: int):
    user_id = get_current_user_id()
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
async def get_liked():
    try:
        user_id = get_current_user_id()

        # Получение лайкнутых мероприятий из базы данных
        liked_events = await ChoicesDAO.liked_events(user_id)
        print(liked_events)

        return JSONResponse(content=liked_events)

    except Exception as e:
        logging.error(f"Ошибка при получении лайкнутых мероприятий: {e}")
        return JSONResponse(content={"error": "Произошла ошибка"}, status_code=500)