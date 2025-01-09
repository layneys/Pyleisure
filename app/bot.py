import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

from app.dao import UsersDAO

# import os
# from dotenv import load_dotenv

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import logging

# load_dotenv()

# TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
# BASE_SITE = os.getenv('BASE_SITE') # Ngrok?

TELEGRAM_API_TOKEN = "your_key"
BASE_SITE = "https://825a-198-244-215-120.ngrok-free.app" # Ngrok?

bot = Bot(token=TELEGRAM_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = f"{BASE_SITE}/webhook"
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    logging.info(f"Webhook set to {webhook_url}")
    yield
    await bot.delete_webhook()
    logging.info("Webhook removed")

class UserForm(StatesGroup):
    telegram_id = State()
    real_name = State()
    username = State()
    city = State()
    age = State()
    gender = State()
    preferences = State()

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(telegram_id=message.from_user.id)
    await state.update_data(username=message.from_user.username or "Не указан")

    await message.answer("Как Вас зовут?")
    await state.set_state(UserForm.real_name)

@dp.message(UserForm.real_name)
async def process_real_name(message: Message, state: FSMContext):
    await state.update_data(real_name=message.text)

    await message.answer("Сколько Вам лет?")
    await state.set_state(UserForm.age)

@dp.message(UserForm.age, F.text.isdigit())
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))

    await message.answer("Из какого Вы города?")
    await state.set_state(UserForm.city)

@dp.message(UserForm.age)
async def invalid_age(message: Message):
    await message.answer("Пожалуйста, введите числовое значение")

@dp.message(UserForm.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    gender_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужской", callback_data="gender:male")],
        [InlineKeyboardButton(text="Женский", callback_data="gender:female")]
    ])
    await message.answer("Какого Вы пола?", reply_markup=gender_keyboard)
    await state.set_state(UserForm.gender)

@dp.callback_query(UserForm.gender, F.data.startswith("gender:"))
async def process_gender(callback: CallbackQuery, state: FSMContext):
    gender = "male" if callback.data == "gender:male" else "female"
    await state.update_data(gender=gender)
    await callback.message.answer("Кратко опишите ваши предпочтения")
    await callback.answer()
    await state.set_state(UserForm.preferences)

@dp.message(UserForm.preferences)
async def process_preferences(message: Message, state: FSMContext):
    await state.update_data(preferences=message.text)

    user_data = await state.get_data()

    await message.answer(
        f"telegram_id: {user_data['telegram_id']}\n"
        f"real_name: {user_data['real_name']}\n"
        f"username: @{user_data['username']}\n"
        f"city: {user_data['city']}\n"
        f"age: {user_data['age']}\n"
        f"gender: {user_data['gender']}\n"
        f"preferences: {user_data['preferences']}"
    )

    await UsersDAO.add(telegram_id=user_data['telegram_id'],
        real_name=user_data['real_name'],
        username=user_data['username'],
        city=user_data['city'],
        age=user_data['age'],
        gender=user_data['gender'],
        preferences=user_data['preferences'],)

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
