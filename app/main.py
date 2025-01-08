from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model.model import LLM_Get_Ans
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
    mocked_prefs = '''
        {
            "preferred_activity": "active",
            "budget": "medium",
            "duration_hours": 3,
            "group_type": "friends",
            "additional_notes": "Prefer outdoor activities"
        }
        '''

    mocked_events = '''
    {
        "event_name": "Summer Jazz Festival",
        "location": "Central Park",
        "date": "2025-07-20",
        "time": "18:00",
        "price_usd": 50
    }
    '''
    mocked_weather = '''
    {
        "city": "New York",
        "temperature_celsius": 25,
        "weather_condition": "sunny",
        "humidity_percent": 60,
        "wind_speed_kmh": 15
    }
    '''

    # model_response = await LLM_Get_Ans(prefs, events, weather, prompt)
    model_response = await LLM_Get_Ans(mocked_prefs, mocked_events, mocked_weather, prompt)

    return templates.TemplateResponse("event_list.html", {"request": request,
                                                          # "events": events,
                                                          # "weather": weather,
                                                          "model_response": model_response})

