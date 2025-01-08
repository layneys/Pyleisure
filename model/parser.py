import asyncio
from logging.config import fileConfig
from sqlalchemy import pool, select
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.dao import UsersDAO, EventsDAO, WeatherDAO
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio
from datetime import date


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
    async def get_data_for_llm():
        #user_data = await asyncio.run(UsersDAO.get_user_data(user_id))

        events_data = await EventsDAO.get_event_data()
        weather_data = await WeatherDAO.get_weather_data('Moscow')
        formatted_user_data, formatted_events_data, formatted_weather_data = format_data_for_llm(events_data, weather_data)
        print(formatted_events_data)
        return formatted_user_data, formatted_events_data, formatted_weather_data

    asyncio.run(get_data_for_llm())
