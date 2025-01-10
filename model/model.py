from dotenv import load_dotenv
import google.generativeai as genai
import json
import os
from typing_extensions import TypedDict, List, Dict
load_dotenv()
  # Загружаем API-ключ из переменной окружения
genai.configure(api_key='AIzaSyC88T1Gurdzk-WpUvd89jYcleM5JI88OY4')

print(dir(genai))

class LLM_Advise(TypedDict):
    event_id: int
    title: str
    description: str
    place: Dict[str, str]
    price: str
    type: str
    img: str
    url: str


async def LLM_Get_Ans(prefs, weather, events, query):
    system_instruction = """Системная инструкция:      Общайся на русском. Ты - помощник для поиска мероприятия для отдыха. 
        Тебе будет дана информация о предпочтениях человека, погоде в его месте нахождения         и проходящих там событиях, мероприятиях и интересных местах в формате JSON. Выбирай строго 
        только из тех мероприятий, которые тебе дают на вход, и только те, которые максимально подходят под описание пользователя. 
        Тебе нужно в соответствии с предпочтениями человека и учитывая его пожелания         сформировать список от пяти до пятнадцати подходящих мероприятий, куда ему можно сходить. 
        Ответ возвращай в формате JSON.         Описание мероприятия должно состоять из 5-8 предложений. 
        Также учитывай сообщение от пользователя. В результирующем файле json должны быть только эти поля:
        event_id: int
        title: str
        description: str
        place: Dict[str, str]
        price: str
        type: str
        img: str
        url: str
"""
    input_message = f"""    Сообщение от пользователя: {query}
    Предпочтения: {prefs}    Погода: {weather}
    События: {events}    """
    try:        # Асинхронный вызов
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json",
        )
        chat = model.start_chat()
        response = chat.send_message(input_message, generation_config=generation_config)
        print(response.text)
        if not response.text:
            print("Empty response from API")
            return None
        response_json = json.loads(response.text)
        print(response_json)
        return response_json
    except json.JSONDecodeError as e:
        print("Error parsing response to JSON:", e)
        print("Raw response:", response.text)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None