from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.misc.json_work import json_read


accept_button = [[InlineKeyboardButton(text="Принять", callback_data="accept")],
                 [InlineKeyboardButton(text="Назад", callback_data="cancel")]]

task_keyboard = InlineKeyboardMarkup(inline_keyboard=accept_button)


def task_preview_keyboard(json_file):
    data = json_read(json_file)
    keyboard = []
    for key in data:
        keyboard.append([InlineKeyboardButton(text=key, callback_data=key)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


task_button = [[InlineKeyboardButton(text="Добавить файлы", callback_data="add_files")],
               [InlineKeyboardButton(text="Отправить на проверку", callback_data="send_to_check")]]

task_work = InlineKeyboardMarkup(inline_keyboard=task_button)
