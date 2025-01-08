from dotenv import load_dotenv
import google.generativeai as genai
import json
import os
from typing import TypedDict, List, Dict

load_dotenv()
genai.configure(api_key='AIzaSyC88T1Gurdzk-WpUvd89jYcleM5JI88OY4')

class LLM_Advise(TypedDict):
    event_id: int
    title: str
    parsed_description: str
    parsed_body_text: str
    price: str
    img: str
    place: Dict[str, str]

async def LLM_Get_Ans(prefs: dict, weather: dict, events: List[dict], query: str):
    system_instruction = """
        Общайся на русском. Ты - помощник для поиска мероприятия для отдыха. 
        Тебе будет дана информация о предпочтениях человека, погоде в его месте нахождения 
        и проходящих там событиях, мероприятиях и интересных местах в формате JSON. 
        Тебе нужно в соответствии с предпочтениями человека и учитывая его пожелания 
        сформировать список от пяти до пятнадцати подходящих мероприятий, куда ему можно сходить. 
        Ответ возвращай в формате JSON. 
        Описание мероприятия должно состоять из 5-8 предложений. 
        Также учитывай сообщение от пользователя.
    """
    input_message = f"""
    Сообщение от пользователя: {query}
    Предпочтения: {json.dumps(prefs, ensure_ascii=False)}
    Погода: {json.dumps(weather, ensure_ascii=False)}
    События: {json.dumps(events, ensure_ascii=False)}
    """
    try:
        response = genai.generate_text(
            model="gemini-1.5-flash",
            messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": input_message}],
            temperature=0.7
        )
        response_json = json.loads(response.result)
        print(response_json)
        return response_json
    except json.JSONDecodeError as e:
        print("Error parsing response to JSON:", e)
        print("Raw response:", response.result)
        return None
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None
