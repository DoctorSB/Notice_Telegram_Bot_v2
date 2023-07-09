from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.database.db import get_task_names_by_worker_id, find_tasks_by_checker_and_status, search_by_status



accept_button = [[InlineKeyboardButton(text="Принять", callback_data="accept")],
                 [InlineKeyboardButton(text="Назад", callback_data="cancel")]]

task_keyboard = InlineKeyboardMarkup(inline_keyboard=accept_button)


def task_preview_keyboard(id):
    data = get_task_names_by_worker_id(id)
    keyboard = []
    for name in data:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=name)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def active_tasks_keyboard():
    data = search_by_status("active")
    keyboard = []
    for name in data:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=name)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


task_button = [[InlineKeyboardButton(text="Добавить файлы", callback_data="add_files")],
               [InlineKeyboardButton(text="Отправить на проверку", callback_data="send_to_check")]]

task_work = InlineKeyboardMarkup(inline_keyboard=task_button)


def tasks_for_review_keyboard(id):
    data = find_tasks_by_checker_and_status(id, "waiting")
    keyboard = []
    for name in data:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=name)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

