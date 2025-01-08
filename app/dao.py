from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from app.database import get_session
from app.models import Users, Events, Companions, Choices, Weather
from datetime import datetime

print(datetime.now().date())

class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, session: get_session(), data_id: int):
        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: get_session(), **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, session: get_session(), **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, session: get_session(), **values):
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
    async def find_user_prefernces_by_id(cls, session: get_session(), data_id: int):
        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


class WeatherDAO(BaseDAO):
    model = Weather


class EventsDAO(BaseDAO):
    model = Events

    @classmethod
    async def delete_irrelevant_events(cls, session: get_session()):
        try:
            # Получение текущей даты
            current_date = datetime.now().date()

            # Удаление событий с датой окончания меньше текущей даты
            stmt = sqlalchemy_delete(Events).where(Events.event_end_date[:11] < str(current_date))
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
