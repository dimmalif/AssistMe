from aiogram import Dispatcher, Bot
from sqlalchemy.orm import sessionmaker

from app.middlewares.database import DatabaseMiddleware


def setup(dp: Dispatcher, environments, session_pool: sessionmaker, bot: Bot):
    dp.setup_middleware(DatabaseMiddleware(session_pool, environments, bot))
