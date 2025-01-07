import asyncio
from logging.config import fileConfig
from sqlalchemy import pool, select
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from database import Base, database_url, async_session
from models import Users, Events, Weather
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

async def get_user_id_by_username(session: AsyncSession, username: str):
    async with session.begin():
        result = await session.execute(
            select(Users.telegram_id).where(Users.username == username)
        )
        user_id = result.scalar_one_or_none()
        return user_id or "Такого пользователя не существует"

async def get_user_data(session: AsyncSession, user_id: int):
    async with session.begin():
        result = await session.execute(
            select(Users).where(Users.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return None
        return {
            "telegram id": user.telegram_id,
            "real name": user.real_name,
            "username": user.username,
            "city": user.city,
            "age": user.age,
            "gender": user.gender,
            "preferences": user.preferences
        }

async def get_event_data(session: AsyncSession):
    async with session.begin():
        result = await session.execute(select(Events))
        events = result.scalars().all()
        return [
            {
                "event_id": event.event_id,
                "event_start_date": event.event_start_date,
                "event_end_date": event.event_end_date,
                "event_type": event.event_type,
                "event_description": event.event_description,
                "event_price": event.event_price,
                "event_img": event.event_img,
                "event_url": event.event_url,
                "event_favorites_count": event.event_favorites_count
            }
            for event in events
        ]

async def get_weather_data(session: AsyncSession, city: str, date: str):
    async with session.begin():
        result = await session.execute(
            select(Weather).where(Weather.city == city, Weather.date == date)
        )
        weather = result.scalar_one_or_none()
        if not weather:
            return None
        return {
            "city": weather.city,
            "date": weather.date,
            "temperature": weather.temperature,
            "description": weather.description,
        }

def format_data_for_llm(user_data, events_data, weather_data):
    formatted_user_data = f"""User Information:
    Telegram ID: {user_data.get('telegram id', 'Unknown')}
    Real Name: {user_data.get('real name', 'Unknown')}
    Username: {user_data.get('username', 'Unknown')}
    City: {user_data.get('city', 'Unknown')}
    Age: {user_data.get('age', 'Unknown')}
    Gender: {user_data.get('gender', 'Unknown')}
    Preferences: {user_data.get('preferences', 'None')}"""
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


async def main():
    async with async_session() as session:
        username = "Michael"
        user_id = await get_user_id_by_username(session, username)
        if isinstance(user_id, str):
            print(user_id)
            return
        user_data = await get_user_data(session, user_id)
        events_data = await get_event_data(session)
        weather_data = await get_event_data(session)
        formatted_user_data, formatted_events_data, formatted_weather_data = format_data_for_llm(user_data, events_data, weather_data)
        print(formatted_user_data)
        print(formatted_events_data)
        print(formatted_weather_data)