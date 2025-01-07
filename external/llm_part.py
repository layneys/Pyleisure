from dotenv import load_dotenv
import google.generativeai as genai
import json
import os
import typing_extensions as typing

load_dotenv()
LLM_API_KEY = os.getenv('MODEL_API_KEY')
genai.configure(api_key=LLM_API_KEY)

class LLM_Advise(typing.TypedDict):
    title: str
    parsed_description: str
    parsed_body_text: str
    is_free: bool
    price: str
    img: str

async def LLM_Get_Ans(prefs, weather, events, query):   
    model = genai.GenerativeModel("gemini-1.5-flash",
        system_instruction="Общайся на русском. Ты - помощник для поиска мероприятия для отдыха. Тебе будет дана информация о предпочтениях человека, погоде в его месте нахождения и проходящих там событиях, мероприятиях и интересных местах в формате json. Тебе нужно в соответствиями с предпочтениями человека и учитывая его пожелания сформировать список от пяти до пятнадцати подходящих мероприятий, куда ему можно сходить. Ответ возвращай в формате json с полями название и описание мероприятия. Описание мероприятия должно состоять из 5-8 предложений. Так же учитывай сообщение от пользователя. Так же запоминай id мероприятия и выводи его в финальный json, чтобы я мог восстановить картинку.")
    chat = model.start_chat()
    response = chat.send_message([
    "Создай список мероприятий на основе этих данных", f"Сообщение от пользователя: {query}", prefs, weather, events],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=list[LLM_Advise]
    ),
)
    try:
        response_json = json.loads(response.text)
        print(response_json)  # Print the parsed JSON
        return response_json
    except json.JSONDecodeError as e:
        print("Error parsing response to JSON:", e)
        print("Raw response:", response.text)
        return None

