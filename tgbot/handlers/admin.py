from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.filters.admin import AdminFilter
from tgbot.database.db import add_task, add_task_files, add_task_worker, get_array_len, get_array_values, get_task_data, get_task_names_by_worker_id, update_task_status, update_task_worker_list


from tgbot.misc.data_formater import date_formater
from tgbot.misc.states import Admin

from tgbot.keyboards.inline import task_preview_keyboard

from tgbot.models.quest import Quest
from tgbot.models.checker import Checker

import datetime

admin_router = Router()
admin_router.message.filter(AdminFilter())
quest = Quest()
checker = Checker()


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Админка!", reply_markup=ReplyKeyboardRemove())


@admin_router.message(Command(commands="remove_checker"))
async def get_remove_checker_id(message: Message, state: FSMContext):  # type: ignore
    await state.set_state(Admin.WAITING_FOR_REMOVE_CHECKER)
    await message.answer("Введите id пользователя, которого хотите сделать проверяющим")


@admin_router.message(Command(commands="create_task"))
async def get_create_task_name(message: Message, state: FSMContext):
    await state.set_state(Admin.WAITING_FOR_TASK_NAME)
    await message.answer("Введите название задания")


@admin_router.message(Admin.WAITING_FOR_TASK_NAME)
async def get_create_task_description(message: Message, state: FSMContext):
    quest.set_quest_name(message.text)
    await message.answer("Введите описание задания")
    await state.set_state(Admin.WAITING_FOR_TASK_DESCRIPTION)


@admin_router.message(Admin.WAITING_FOR_TASK_DESCRIPTION)
async def get_create_task_time(message: Message, state: FSMContext):
    quest.set_quest_description(message.text)
    await message.answer("Введите время на выполнение задания в формате\nдень месяц год час минута")
    await state.set_state(Admin.WAITING_FOR_TASK_TIME_LIMIT)


@admin_router.message(Admin.WAITING_FOR_TASK_TIME_LIMIT)
async def create_task(message: Message, state: FSMContext):
    try:
        date = date_formater(message.text)
    except:
        await message.answer("Неверный формат даты")
        return
    quest.set_quest_status("active")
    quest.set_time_limit(str(date))
    quest.set_checker_id(message.from_user.id)
    await state.clear()
    add_task(quest.get_quest_name(), quest.get_quest_description(
    ), quest.get_quest_status(), quest.get_time_limit(), quest.get_checker_id())
    await message.answer(f"Задание создано")


@admin_router.message(Command(commands="add_executor"))
async def add_executor(message: Message, state: FSMContext):
    await message.answer("Выберете задание для добавления исполнителя", reply_markup=task_preview_keyboard('tasks.json'))
    await state.set_state(Admin.WAITING_FOR_TASK_ID)


@admin_router.callback_query(Admin.WAITING_FOR_TASK_ID)
async def get_task_id(query, state: FSMContext):
    update_task_worker_list(query.data, query.from_user.id)
    await query.message.edit_text(f"Исполнитель добавлен")
    await state.set_state(Admin.WAITING_FOR_ADD_EXECUTOR)


@admin_router.message(Admin.WAITING_FOR_ADD_EXECUTOR)
async def add_executor_id(message: Message, state: FSMContext):
    info = await state.get_data()
    add_task_worker(info['task_id'], message.forward_from.id)
    await state.clear()
