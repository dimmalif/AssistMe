import asyncio
import logging
from sqlalchemy import select
import aiogram
import betterlogging as bl
import pyrogram
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode, AllowedUpdates, BotCommand

from app import handlers, middlewares, filters
from app.config import Config
from app.database.models import Operator
from app.database.services.db_engine import create_db_engine_and_session_pool
from app.userbot import UserbotController

log = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand('start', '[Re]Start bot')
        ]
    )
    log.info("Installation of commands was successful")


async def notify_admin(bot: Bot, admin_ids: tuple[int]) -> None:
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, 'Bot launched')
        except aiogram.exceptions.ChatNotFound:
            log.warning(f'Admin from {admin_id} did not initialize the chat.')


async def main():
    config = Config.from_env()
    bl.basic_colorized_config(level=config.misc.log_level)
    log.info('Im starting...')

    storage = MemoryStorage()
    bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    db_engine, sqlalchemy_session = await create_db_engine_and_session_pool(config.db.sqlalchemy_url)

    userbot = UserbotController(config.userbot, (await bot.me).username, 'app/static/chat_photo.png')

    allowed_updates = (
            AllowedUpdates.MESSAGE + AllowedUpdates.CALLBACK_QUERY +
            AllowedUpdates.EDITED_MESSAGE + AllowedUpdates.CHAT_JOIN_REQUEST +
            AllowedUpdates.PRE_CHECKOUT_QUERY + AllowedUpdates.SHIPPING_QUERY +
            AllowedUpdates.INLINE_QUERY
    )
    environments = dict(config=config, dp=dp, userbot=userbot)
    handlers.setup(dp)
    middlewares.setup(dp, environments, sqlalchemy_session, bot)
    filters.setup(dp)
    await set_bot_commands(bot)
    await notify_admin(bot, config.bot.admin_ids)

    try:
        await dp.skip_updates()
        await dp.start_polling(allowed_updates=allowed_updates, reset_webhook=True)
    finally:
        await storage.close()
        await storage.wait_closed()
        await (await bot.get_session()).close()
        await db_engine.dispose()
        await userbot._client.stop()

if __name__ == '__main__':

    def get_peer_type(peer_id: int) -> str:
        peer_id_str = str(peer_id)
        if not peer_id_str.startswith("-"):
            return "user"
        elif peer_id_str.startswith("-100"):
            return "channel"
        else:
            return "chat"


    pyrogram.utils.get_peer_type = get_peer_type

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.warning('The bot is stopped')
