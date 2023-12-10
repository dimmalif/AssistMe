from aiogram import Bot
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.services.repos import LeadRepo, OperatorRepo


class DatabaseMiddleware(LifetimeControllerMiddleware):
    def __init__(self, session_pool: sessionmaker, environments, bot: Bot):
        self.session_pool = session_pool
        self.environments = environments
        self.bot = bot
        super().__init__()

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        session: AsyncSession = self.session_pool()
        data['session'] = session
        data['userbot'] = self.environments['userbot']
        data['lead_db'] = LeadRepo(session)
        data['operator_db'] = OperatorRepo(session)
        data['bot'] = self.bot
        # operator_db = OperatorRepo(session)
        # all_operators = await operator_db.get_all()
        # print(all_operators)

    async def post_process(self, obj, data, *args):
        if session := data.get('session', None):
            session: AsyncSession
            await session.close()
