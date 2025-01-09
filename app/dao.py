from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, String
from app.database import async_session
from app.models import Users, Events, Companions, Choices, Weather
from datetime import datetime
from sqlalchemy.sql.expression import cast

print(datetime.now().date())

class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        async with async_session() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def find_user_prefernces_by_id(cls, data_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_user_id_by_username(cls, username: str):
        async with async_session() as session:
            result = await session.execute(
                select(Users.telegram_id).where(Users.username == username)
            )
            user_id = result.scalar_one_or_none()
            return user_id or "Такого пользователя не существует"

    @classmethod
    async def get_user_data(cls, user_id: int):
        async with async_session() as session:
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


class WeatherDAO(BaseDAO):
    model = Weather

    @classmethod
    async def get_weather_data(cls, city: str):
        async with async_session() as session:
            result = await session.execute(
                select(Weather).where(Weather.city == city)
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

    @classmethod
    async def delete_irrelevant_weather(cls):
        async with async_session() as session:
            stmt = sqlalchemy_delete(Weather)
            result = await session.execute(stmt)

            # Подтверждение изменений
            await session.commit()


class EventsDAO(BaseDAO):
    model = Events

    @classmethod
    async def get_event_data(cls):
        async with async_session() as session:
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

    @classmethod
    async def delete_irrelevant_events(cls):
        async with async_session() as session:
            try:
                # Получение текущей даты
                current_date = datetime.now()

                # Удаление событий с датой окончания меньше текущей даты
                stmt = sqlalchemy_delete(Events).where(Events.event_end_date < current_date.strftime("%Y-%m-%d %H:%M:%S"))
                result = await session.execute(stmt)

                # Подтверждение изменений
                await session.commit()

                print(f"Удалено мероприятий: {result.rowcount}")
            except Exception as e:
                await session.rollback()  # Откат изменений в случае ошибки
                print(f"Ошибка при удалении старых мероприятий: {e}")

class CompanionsDAO(BaseDAO):
    model = Companions

class ChoicesDAO(BaseDAO):
    model = Choices

    @classmethod
    async def liked_events(cls, telegram_id: int):
        async with async_session() as session:
            query = select(Choices).join(Events).where(Choices.telegram_id == telegram_id)
            result = await session.execute(query)
            liked_events = result.scalars().all()
            return liked_events