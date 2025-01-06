from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from external.events import get_events_page
from external.weather import get_weather


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
):
    events = await get_events_page(choice)
    weather = await get_weather(choice)

    return templates.TemplateResponse("event_list.html", {"request": request,
                                                          "events": events,
                                                          "weather": weather})

