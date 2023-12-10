from aiogram import Dispatcher

from app.handlers import private, operator, pyrogram


def setup(dp: Dispatcher):
    private.setup(dp)
    operator.setup(dp)
    pyrogram.setup(dp)


