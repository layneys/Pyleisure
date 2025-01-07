from sqlalchemy import String, BigInteger, Integer, Date, Time, ForeignKey, Enum, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class Users(Base):
    __tablename__ = 'users'

    class GenderEnum(enum.Enum):
        male = 'М'
        female = 'Ж'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Уникальный идентификатор пользователя в Telegram
    real_name: Mapped[str] = mapped_column(String, nullable=True)  # Имя пользователя
    username: Mapped[str] = mapped_column(String, nullable=False)  # Telegram username
    age: Mapped[int] = mapped_column(Integer, nullable=False)   # возраст пользователя
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum), nullable=False)   # пол пользователя
    preferences: Mapped[JSONB] = mapped_column(JSONB, nullable=True)   # предпочтения пользователя

    # Связь с таблицами
    templates: Mapped[list["Templates"]] = relationship(back_populates="user")
    groups: Mapped[list["Companions"]] = relationship(back_populates="user")
    choices: Mapped[list["Choices"]] = relationship(back_populates="user")

class Templates(Base):
    __tablename__ = 'templates'

    class TimeOfDay(enum.Enum):
        morning = 'Утро'
        day = 'День'
        evening = 'Вечер'
        night = 'Ночь'

    template_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id'))
    range: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    time: Mapped[TimeOfDay] = mapped_column(Enum(TimeOfDay), nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped["Users"] = relationship(back_populates="templates")


class Events(Base):
    __tablename__ = 'events'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_date: Mapped[Date] = mapped_column(Date, nullable=False)
    event_time: Mapped[Time] = mapped_column(Time, nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    event_price: Mapped[float] = mapped_column(Float, nullable=False)

    choices: Mapped[list["Choices"]] = relationship(back_populates="event")  # надо сделать 1 к 1


class Weather(Base):
    __tablename__ = 'weather'

    city: Mapped[str] = mapped_column(String, primary_key=True)
    date: Mapped[Date] = mapped_column(Date, primary_key=True)
    temperature: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

class Companions(Base):
    __tablename__ = 'companions'

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id'))
    members_ids: Mapped[JSONB] = mapped_column(JSONB, nullable=False)

    user: Mapped["Users"] = relationship(back_populates="groups")
    choices: Mapped[list["Choices"]] = relationship(back_populates="groups")


class Choices(Base):
    __tablename__ = 'choices'

    choice_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id'))
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.event_id'))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('companions.group_id'))

    user: Mapped["Users"] = relationship(back_populates="choices")
    events: Mapped["Events"] = relationship(back_populates="choices")
    groups: Mapped["Companions"] = relationship(back_populates="choices")

