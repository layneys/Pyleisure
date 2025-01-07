from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from external.events import get_events_page
from external.weather import get_weather
from external.llm_part import LLM_Get_Ans

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/list", response_class=HTMLResponse)
async def process_data(
    request: Request,
    choice: str = Form(...)
    #user_query: str = Form(...) нужен запрос от пользователя, его пожелание\\\\ или не нужен???
):


    events = await get_events_page(choice)
    weather = await get_weather(choice)

    # Fetch preferences, weather, and events
    #prefs = await get_prefs(user_query)  # Берем из БД. Здесь??
    #weather = await get_weather(city)
    #events = await get_events_page(city)

    # Call LLM for recommendations
    recommendations = await LLM_Get_Ans(prefs, weather, events, user_query)

    return templates.TemplateResponse("event_list.html", {"request": request,
                                                          "events": events,
                                                          "weather": weather,
                                                          "recommendations": recommendations})

