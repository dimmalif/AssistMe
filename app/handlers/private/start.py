from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.database.services.repos import LeadRepo
from app.filters import IsAdminFilter
from app.keyboards.inline.inline_markup.users.main_menu import main_menu_kb, registration_kb


async def start_cmd(message: Message, lead_db: LeadRepo):
    is_register = await lead_db.get_user(user_id=message.from_user.id)
    if not is_register:
        text = 'Welcome to AssistMe_bot!\n' \
               'You are not registered. To do this, share your contact using the button below'
        await message.answer(text=text, reply_markup=registration_kb())
    else:
        text = 'Welcome to AssistMeBot.\nTo start communicating with the operator just click the button ' \
               '"Start a chat with an operator"☺\n'
        await message.answer(text=text, reply_markup=main_menu_kb())


async def registration(message: Message, lead_db: LeadRepo):
    if message.from_user.id == message.contact.user_id:
        is_register = await lead_db.get_user(user_id=message.from_user.id)
        if not is_register:
            await lead_db.add(user_id=message.contact.user_id, username=message.from_user.full_name,
                              tag=message.from_user.username, phone_number=message.contact.phone_number)
        text = 'Welcome to AssistMeBot.\nTo start communicating with the operator just click the button ' \
               '"Start a chat with an operator"☺\n'
        await message.answer(text=text, reply_markup=main_menu_kb())
    else:
        await message.answer(text='You didnt send your contact, thats not how it works)')


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart(), IsAdminFilter(), state='*')
    dp.register_message_handler(registration, content_types=types.ContentType.CONTACT, state='*')
