from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.keyboards.inline.inline_markup.base import *

main_menu_cb = CallbackData('mm', 'action')


def main_menu_kb():
    def button_cb(action: str):
        return dict(callback_data=main_menu_cb.new(action=action))

    inline_keyboard = [
        [InlineKeyboardButton(Buttons.user_main_menu.start_chat, **button_cb('start_chat'))]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


registration_cb = CallbackData('rg', 'action')


def registration_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Send phone number📱", request_contact=True))

    return keyboard


accept_invite_cb = CallbackData('ai', 'action')


def accept_invite_kb(invite_link):
    def button_cb(action: str):
        return dict(callback_data=accept_invite_cb.new(action=action))

    inline_keyboard = [
        [InlineKeyboardButton(Buttons.user_main_menu.accept_invite, **button_cb('accept_invite'), url=invite_link)]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
