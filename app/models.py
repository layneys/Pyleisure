from sqlalchemy import String, BigInteger, Integer, Date, Time, ForeignKey, Enum, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class Users(Base):
    __tablename__ = 'users'

    class GenderEnum(enum.Enum):
        male = 'Мужской'
        female = 'Женский'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Уникальный идентификатор пользователя в Telegram
    real_name: Mapped[str] = mapped_column(String, nullable=True)  # Имя пользователя
    username: Mapped[str] = mapped_column(String, nullable=False)  # Telegram username
    city: Mapped[str] = mapped_column(String, nullable=True)  # Город пользователя
    age: Mapped[int] = mapped_column(Integer, nullable=True)   # возраст пользователя
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum), nullable=True)   # пол пользователя
    preferences: Mapped[str] = mapped_column(String, nullable=True)   # предпочтения пользователя

    # Связь с таблицами
    groups: Mapped[list["Companions"]] = relationship(back_populates="user")
    choices: Mapped[list["Choices"]] = relationship(back_populates="user")

class Events(Base):
    __tablename__ = 'events'

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_title: Mapped[str] = mapped_column(String, nullable=False)
    event_city: Mapped[str] = mapped_column(String, nullable=False)
    event_place: Mapped[str] = mapped_column(String, nullable=False)
    event_start_date: Mapped[str] = mapped_column(String, nullable=False)
    event_end_date: Mapped[str] = mapped_column(String, nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    event_description: Mapped[str] = mapped_column(String, nullable=False)
    event_price: Mapped[str] = mapped_column(String, nullable=False)
    event_img: Mapped[str] = mapped_column(String, nullable=False)
    event_url: Mapped[str] = mapped_column(String, nullable=False)
    event_favorites_count: Mapped[int] = mapped_column(Integer, nullable=False)

    choices: Mapped[list["Choices"]] = relationship(back_populates="events", cascade="all, delete-orphan")


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

    #choice_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id'), primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.event_id'), primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('companions.group_id'), nullable=True)

    user: Mapped["Users"] = relationship(back_populates="choices")
    events: Mapped["Events"] = relationship(back_populates="choices")
    groups: Mapped["Companions"] = relationship(back_populates="choices")

