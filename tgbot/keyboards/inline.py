from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.misc.json_work import json_read
from tgbot.database.db import add_task, add_task_files, add_task_worker, get_array_len, get_array_values, get_task_data, get_task_names_by_worker_id, update_task_status, update_task_worker_list



accept_button = [[InlineKeyboardButton(text="Принять", callback_data="accept")],
                 [InlineKeyboardButton(text="Назад", callback_data="cancel")]]

task_keyboard = InlineKeyboardMarkup(inline_keyboard=accept_button)


def task_preview_keyboard(id):
    data = get_task_names_by_worker_id(id)
    keyboard = []
    for name in data:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=name)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


task_button = [[InlineKeyboardButton(text="Добавить файлы", callback_data="add_files")],
               [InlineKeyboardButton(text="Отправить на проверку", callback_data="send_to_check")]]

task_work = InlineKeyboardMarkup(inline_keyboard=task_button)
