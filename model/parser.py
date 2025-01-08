import asyncio
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session
from app.dao import UsersDAO, EventsDAO, WeatherDAO
from aiogram.types import Message

def format_data_for_llm(events_data, weather_data):
    formatted_user_data = f"""User Information:"""
    # Telegram ID: {user_data.get('telegram id', 'Unknown')}
    # Real Name: {user_data.get('real name', 'Unknown')}
    # Username: {user_data.get('username', 'Unknown')}
    # City: {user_data.get('city', 'Unknown')}
    # Age: {user_data.get('age', 'Unknown')}
    # Gender: {user_data.get('gender', 'Unknown')}
    # Preferences: {user_data.get('preferences', 'None')}"""
    formatted_events_data = "Events:\n"
    if events_data:
        for event in events_data:
            formatted_events_data += (
                f"- Event ID: {event['event_id']}\n"
                f"  Start Date: {event['event_start_date']}\n"
                f"  End Date: {event['event_end_date']}\n"
                f"  Type: {event['event_type']}\n"
                f"  Description: {event['event_description']}\n"
                f"  Price: {event['event_price']}\n"
                f"  Image: {event['event_img']}\n"
                f"  URL: {event['event_url']}\n"
                f"  Favorites Count: {event['event_favorites_count']}\n\n"
            )
    else:
        formatted_events_data += "No events available.\n"
    formatted_weather_data = "Weather:\n"
    if weather_data:
        formatted_weather_data += (
            f"City: {weather_data['city']}\n"
            f"Date: {weather_data['date']}\n"
            f"Temperature: {weather_data['temperature']}°C\n"
            f"Description: {weather_data['description']}\n"
        )
    else:
        formatted_weather_data += "No weather data available.\n"
    return formatted_user_data, formatted_events_data, formatted_weather_data

if __name__ == '__main__':
    async def get_info():
        user_data = await UsersDAO.get_user_data(Message.from_user.id)
        if not user_data:
            return "Пользователь не найден."
        current_date = datetime.now().strftime("%Y-%m-%d")
        events_data = await EventsDAO.get_event_data()
        weather_data = await WeatherDAO.get_weather_data(user_data["city"])
        formatted_user_data, formatted_events_data, formatted_weather_data = format_data_for_llm(
            user_data, events_data, weather_data
        )
        return formatted_user_data, formatted_events_data, formatted_weather_data
        formatted_data = await process_user_data(message)
        if isinstance(formatted_data, str):
            print(formatted_data)
        else:
            formatted_user_data, formatted_events_data, formatted_weather_data = formatted_data
            print(formatted_user_data)
            print(formatted_events_data)
            print(formatted_weather_data)

