from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message

from app.config import Config


class IsAdminFilter(BoundFilter):

    async def check(self, upd: Message, *args: ...) -> bool:
        data: dict = ctx_data.get()
        print(upd.from_user.id)
        if 'config' not in data:
            config = Config.from_env()
            if upd.from_user.id in config.bot.admin_ids:
                return False
            else:
                return True

        config: Config = data['config']
        return upd.from_user.id in config.bot.admin_ids
