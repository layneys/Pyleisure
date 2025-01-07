from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.dao import UsersDAO
#from app.bot.keyboards.kbs import app_keyboard
#from app.bot.utils.utils import greet_user, get_about_us_text

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Обрабатывает команду /start.
    """
    user = await UsersDAO.find_one_or_none(telegram_id=message.from_user.id)

    if not user:
        await UsersDAO.add(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,

        )