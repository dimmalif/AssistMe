from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.models import Operator
from app.database.services.repos import LeadRepo, OperatorRepo
from app.keyboards.inline.inline_markup.admin.main_menu import operator_main_kb, operator_main_cb
from app.keyboards.inline.inline_markup.users.main_menu import main_menu_cb, accept_invite_kb
from app.states.states import ChatRepo
from app.userbot import UserbotController


async def attention_operators(all_operators, current_user, call: CallbackQuery, bot):
    for i in all_operators:
        text = f'New request!\nid of user: {call.from_user.id}\n' \
               f'User tag: {call.from_user.full_name}\n' \
               f'User phone number: {current_user.phone_number}'
        try:
            await bot.send_message(i.user_id, text)
        except:
            text = f'Operator {i.user_id}, {i.tag}, {i.username} - didnt start chat with bot!!'
            for j in all_operators:
                try:
                    await bot.send_message(j.user_id, text)
                except:
                    pass


def sort_operators(all_operators) -> Operator | None:
    chill_operators = [operator for operator in all_operators if not operator.active_chat_links
                       and operator.is_active == 'active']
    active_operators = [operator for operator in all_operators if operator.active_chat_links and operator.is_active ==
                        'active']
    active_operators = [operator for operator in active_operators if
                        len(str(operator.active_chat_links).split(', ')) < 6]
    active_operators.sort(key=lambda operator: len(str(operator.active_chat_links).split(', ')))
    if chill_operators:
        return chill_operators[0]
    elif active_operators:
        return active_operators[0]
    else:
        return None


async def new_chat_reqeust(call: CallbackQuery, lead_db: LeadRepo, operator_db: OperatorRepo,
                           userbot: UserbotController, bot: Bot):
    await call.answer('Your request has been sent')
    current_user = await lead_db.get_user(user_id=call.from_user.id)
    all_operators = await operator_db.get_all()
    need_operator = sort_operators(all_operators)
    if current_user.waiting_status == 'waiting' and not need_operator:
        await call.message.answer('Youre already in line. Please wait, someone will be released soon')
        return

    if not need_operator:
        await attention_operators(all_operators=all_operators, current_user=current_user, call=call, bot=bot)
        await call.message.answer('All operators are busy at the moment, please wait.\nAverage waiting time'
                                  ' - 3 minutes.')
        await lead_db.update_user(user_id=call.from_user.id, waiting_status='waiting')
    else:

        if current_user.waiting_status == 'create_chat' or current_user.waiting_status == 'accepted':
            await call.message.answer('You have already created a chat. Join us!☺',
                                      reply_markup=accept_invite_kb(current_user.active_chat_link))
            await lead_db.update_user(user_id=call.from_user.id, operator_id=need_operator.user_id)
        else:
            chat, invite_link, room_name = await userbot.create_new_room(last_room_number=call.from_user.id)
            await call.message.answer('Chat has been created, join us☺\n',
                                      reply_markup=accept_invite_kb(invite_link.invite_link))

            await lead_db.update_user(user_id=call.from_user.id, waiting_status='create_chat',
                                      active_chat_link=invite_link.invite_link, active_chat_id=chat.id,
                                      operator_id=need_operator.user_id)


async def approve_join_req(update: types.ChatJoinRequest, operator_db: OperatorRepo, lead_db: LeadRepo,
                           userbot: UserbotController, bot: Bot):
    current_user = await lead_db.get_user(update.from_user.id)
    current_operator = await operator_db.get_user(user_id=current_user.operator_id)
    if current_operator.is_active != 'active':
        await bot.send_message(current_user.user_id, 'Sorry, there was an error.'
                                                     ' Restart the bot with /start and try again.')
        return
    await update.approve()
    await userbot.add_chat_member(chat_id=current_user.active_chat_id, user_id=current_user.operator_id)
    await bot.send_message(current_user.operator_id, 'New chat! Join him',
                           reply_markup=accept_invite_kb(current_user.active_chat_link))

    all_operator_links = current_operator.active_chat_links + f', {current_user.active_chat_link}' if \
        current_operator.active_chat_links else current_user.active_chat_link

    await operator_db.update_user(user_id=current_operator.user_id, active_chat_links=all_operator_links)
    await lead_db.update_user(user_id=update.from_user.id, waiting_status='accepted')


async def init_start_que_chat(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Enter user id')
    await state.update_data(start_init=True)
    await ChatRepo.StartInitChat.set()


async def finalize_start_que_chat(message: Message, lead_db: LeadRepo, operator_db: OperatorRepo,
                                  userbot: UserbotController, state: FSMContext, bot: Bot):
    current_operator = await operator_db.get_user(user_id=message.from_user.id)
    current_user = await lead_db.get_user(user_id=int(message.text))
    if not current_user:
        text = 'Welcome to AssistMeBot. You are in the admin panel☺\nUser not found'
        await message.answer(text, reply_markup=operator_main_kb())
    elif current_user.waiting_status != 'waiting':
        text = 'Welcome to AssistMeBot. You are in the admin panel☺\nThe selected user is not in the queue!'
        await message.answer(text, reply_markup=operator_main_kb())
    else:
        chat, invite_link, room_name = await userbot.create_new_room(last_room_number=int(message.text))
        await message.answer(
            'The chat has been created. When a user joins you will be added automatically☺\n',
            reply_markup=operator_main_kb())
        await bot.send_message(message.text, text='Chat has been created, join us☺\n',
                               reply_markup=accept_invite_kb(invite_link.invite_link))
        await lead_db.update_user(user_id=current_user.user_id, waiting_status='create_chat',
                                  active_chat_link=invite_link.invite_link, active_chat_id=chat.id,
                                  operator_id=current_operator.user_id)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(new_chat_reqeust, main_menu_cb.filter(action='start_chat'), state='*')
    dp.register_chat_join_request_handler(approve_join_req, state='*')
    dp.register_callback_query_handler(init_start_que_chat, operator_main_cb.filter(action='start_queue_chat'),
                                       state='*')
    dp.register_message_handler(finalize_start_que_chat, state=ChatRepo.StartInitChat)

