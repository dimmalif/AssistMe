from aiogram import Dispatcher

import logging

from app.filters.admin import *

log = logging.getLogger(__name__)


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdminFilter, event_handlers=[dp.message_handlers, dp.callback_query_handlers])
    log.info('Фільтри встановлені успішно...')
