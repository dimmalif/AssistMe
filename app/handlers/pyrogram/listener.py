import os

from aiogram import Dispatcher, types, Bot
from aiogram.types import Message

from app.userbot import UserbotController


def create_folder(chat_name):
    user_folder_path = f'chats/{chat_name}'
    os.makedirs(user_folder_path, exist_ok=True)
    file_path = os.path.join(user_folder_path, 'messages.txt')
    return file_path


async def listen_messages(message: Message):
    with open(create_folder(message.chat.full_name), mode='a+', encoding='utf-8') as f:
        f.write(f'Sent: {message.from_user.username}.')
        if 'edit_date' in message.values:
            f.write('Changed message. ')
            date = message.edit_date
        else:
            date = message.date
        f.write(f'Date: {date} //// Text:\n{message.text}\n')


async def listen_document(message: Message, bot: Bot):
    chat_folder = os.path.join('chats', message.chat.full_name)
    photos_folder = os.path.join(chat_folder, 'photos')

    os.makedirs(photos_folder, exist_ok=True)

    file_info = await bot.get_file(message.photo[-1].file_id)
    file_name = f"{message.from_user.full_name}--{file_info.file_unique_id}.jpg"

    absolute_file_path = os.path.join(photos_folder, file_name)

    await bot.download_file(file_info.file_path, absolute_file_path)


async def listen_voice(message: Message, bot: Bot):
    chat_folder = os.path.join('chats', message.chat.full_name)
    voices_folder = os.path.join(chat_folder, 'voices')

    os.makedirs(voices_folder, exist_ok=True)

    file_info = await bot.get_file(message.voice.file_id)
    file_name = f"{message.from_user.full_name}--{file_info.file_unique_id}.mp4"

    absolute_file_path = os.path.join(voices_folder, file_name)

    await bot.download_file(file_info.file_path, absolute_file_path)


def setup(dp: Dispatcher):
    dp.register_message_handler(listen_messages, state='*')
    dp.register_edited_message_handler(listen_messages, state='*')

    dp.register_message_handler(listen_document, content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT],
                                state='*')
    dp.register_message_handler(listen_voice, content_types=[types.ContentType.VOICE, types.ContentType.AUDIO])
