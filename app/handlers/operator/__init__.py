from aiogram import Dispatcher

from app.handlers.operator import main_menu
from app.handlers.pyrogram import chat_init


def setup(dp: Dispatcher):
    main_menu.setup(dp)
    chat_init.setup(dp)
