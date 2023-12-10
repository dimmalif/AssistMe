from app.keyboards.inline.inline_markup.base import *

operator_start_cb = CallbackData('os', 'action')


def operator_start_kb():
    def button_cb(action: str):
        return dict(callback_data=operator_start_cb.new(action=action))

    inline_keyboard = [
        [InlineKeyboardButton(Buttons.operator_start_menu.start_work, **button_cb('start_work'))]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


operator_main_cb = CallbackData('om', 'action')


def operator_main_kb(que_exists=False):
    def button_cb(action: str):
        return dict(callback_data=operator_main_cb.new(action=action))

    inline_keyboard = [
        [InlineKeyboardButton(Buttons.operator_main_menu.stop_chat, **button_cb('stop_chat'))],
        [InlineKeyboardButton(Buttons.operator_main_menu.que_status, **button_cb('que_status'))],
        [InlineKeyboardButton(Buttons.operator_main_menu.finalize_work, **button_cb('finalize_work'))],
    ]
    if que_exists:
        inline_keyboard.append([InlineKeyboardButton(Buttons.operator_main_menu.start_queue_chat,
                                                     **button_cb('start_queue_chat'))])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
