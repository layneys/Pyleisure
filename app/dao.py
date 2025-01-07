from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from app.database import get_session
from app.models import Users, Templates, Events, Companions, Choices, Weather

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

class TemplatesDAO(BaseDAO):
    model = Templates

class WeatherDAO(BaseDAO):
    model = Weather

class EventsDAO(BaseDAO):
    model = Events

class CompanionsDAO(BaseDAO):
    model = Companions

class ChoicesDAO(BaseDAO):
    model = Choices