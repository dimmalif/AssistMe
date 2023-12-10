from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.database.services.repos import OperatorRepo, LeadRepo
from app.keyboards.inline.inline_markup.admin.main_menu import operator_start_kb, operator_start_cb, operator_main_kb, \
    operator_main_cb
from app.states.states import ChatRepo
from app.userbot import UserbotController


async def start_cmd(message: Message, operator_db: OperatorRepo):
    current_operator = await operator_db.get_user(user_id=message.from_user.id)
    text = 'Welcome to AssistMeBot. You are in the admin panel☺\n'
    if current_operator.is_active == 'inactive':
        await message.answer(text=text, reply_markup=operator_start_kb())
    else:
        try:
            current_operator = await operator_db.get_user(user_id=message.from_user.id)
            text = 'Welcome to AssistMeBot. You are in the admin panel☺\nActive chats:\n' + ''.join(
                f'{i}\n' for i in current_operator.active_chat_links.split(', '))
            await message.answer(text=text, reply_markup=operator_main_kb())
        except Exception:
            print('27 line')


async def finalize_work(call: CallbackQuery, operator_db: OperatorRepo):
    current_operator = await operator_db.get_user(user_id=call.from_user.id)
    try:
        await call.message.edit_text(
            text='Welcome to AssistMeBot. You are in the admin panel☺\nYou are not working at the moment',
            reply_markup=operator_start_kb())
    except:
        print('35 line')
    if current_operator.is_active == 'active':
        await operator_db.update_user(user_id=call.from_user.id, is_active='inactive')
        text = 'Welcome to AssistMeBot. You are in the admin panel☺\n'
        await call.message.edit_text(text=text, reply_markup=operator_start_kb())


async def main_menu_cmd(call: CallbackQuery, operator_db: OperatorRepo):
    try:
        current_operator = await operator_db.get_user(user_id=call.from_user.id)

        text = 'Welcome to AssistMeBot. You are in the admin panel☺\nActive chats:\n' + ''.join(
            f'{i}\n' for i in current_operator.active_chat_links.split(', '))
        await call.message.edit_text(text=text, reply_markup=operator_main_kb())
    except:
        print('50 line')

    await operator_db.update_user(user_id=call.from_user.id, is_active='active')


async def init_stop_chat(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Write a link to the chat you want to end')
    await state.update_data(start_del_chat=True)
    await ChatRepo.StartDelChat.set()


async def finalize_stop_chat(message: Message, state: FSMContext, lead_db: LeadRepo, operator_db: OperatorRepo,
                             userbot: UserbotController):
    # region update operator active_chat_links
    current_operator = await operator_db.get_user(user_id=message.from_user.id)
    operator_links: str = current_operator.active_chat_links
    all_links = [link.strip() for link in operator_links.split(',')]
    if message.text in all_links:
        all_links.remove(message.text)
    updated_links = ', '.join(all_links)
    await operator_db.update_user(user_id=current_operator.user_id, active_chat_links=updated_links)
    # endregion
    # region update user data
    await lead_db.update_waiting_status(link=message.text, waiting_status='finalize')
    # endregion
    # region del chat
    chat_id = await lead_db.get_chat_id(link=message.text)
    if not chat_id:
        text = 'Welcome to AssistMeBot. You are in the admin panel☺\nInvalid chat link entered, try again' \
               '\nActive chats:' + ''.join(f'{i}\n' for i in current_operator.active_chat_links.split(', '))
        await message.answer(text=text, reply_markup=operator_main_kb())
        return
    await userbot.delete_group(chat_id=chat_id)
    # endregion
    text = 'Welcome to AssistMeBot. You are in the admin panel☺\nChat ended\nActive chats:\n' + ''.join(
        f'{i}\n' for i in current_operator.active_chat_links.split(', '))
    await message.answer(text, reply_markup=operator_main_kb())
    await state.finish()


async def check_queue(call: CallbackQuery, lead_db: LeadRepo, operator_db: OperatorRepo):
    leads_waiting = await lead_db.get_waiting_user()
    current_operator = await operator_db.get_user(user_id=call.from_user.id)
    if not leads_waiting:
        text = 'Welcome to AssistMeBot. You are in the admin panel☺\nThere is no one in the queue\nActive chats:\n' + \
               ''.join(f'{i}\n' for i in current_operator.active_chat_links.split(', '))
        await call.message.edit_text(text=text, reply_markup=operator_main_kb())
    else:
        text = 'Welcome to AssistMeBot. You are in the admin panel☺\nThe following users are currently in the queue:\n'\
               + ''.join([f'user_id: {i.user_id}\nuser tag: @{i.tag}' for i in leads_waiting])
        await call.message.edit_text(text=text, reply_markup=operator_main_kb(que_exists=True))


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
    dp.register_callback_query_handler(main_menu_cmd, operator_start_cb.filter(action='start_work'), state='*')
    dp.register_callback_query_handler(finalize_work, operator_main_cb.filter(action='finalize_work'), state='*')
    dp.register_callback_query_handler(init_stop_chat, operator_main_cb.filter(action='stop_chat'), state='*')
    dp.register_message_handler(finalize_stop_chat, state=ChatRepo.StartDelChat)
    dp.register_callback_query_handler(check_queue, operator_main_cb.filter(action='que_status'), state='*')
