from aiogram import Dispatcher

from app.handlers.pyrogram import chat_init, listener


def setup(dp: Dispatcher):
    chat_init.setup(dp)
    listener.setup(dp)
