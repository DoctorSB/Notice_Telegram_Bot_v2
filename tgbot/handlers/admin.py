from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter
from tgbot.database.db import add_task, add_task_worker


from tgbot.misc.data_formater import date_formater
from tgbot.misc.states import Admin

from tgbot.keyboards.inline import task_preview_keyboard
from tgbot.keyboards.reply import admin_keyboard


import os


admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message, state: FSMContext):
    await message.reply("Вы проверяющий", reply_markup=admin_keyboard)
    await state.clear()


@admin_router.message(F.text == "Создать задание")
async def get_create_task_name(message: Message, state: FSMContext):
    await state.set_state(Admin.WAITING_FOR_TASK_NAME)
    await message.answer("Введите название задания")


@admin_router.message(Admin.WAITING_FOR_TASK_NAME)
async def get_create_task_description(message: Message, state: FSMContext):
    await state.update_data(task_name=message.text)
    await message.answer("Введите описание задания")
    await state.set_state(Admin.WAITING_FOR_TASK_DESCRIPTION)


@admin_router.message(Admin.WAITING_FOR_TASK_DESCRIPTION)
async def get_create_task_time(message: Message, state: FSMContext):
    await state.update_data(task_description=message.text)
    await message.answer("Введите время на выполнение задания в формате\nдень месяц год час минута")
    await state.set_state(Admin.WAITING_FOR_TASK_TIME_LIMIT)


@admin_router.message(Admin.WAITING_FOR_TASK_TIME_LIMIT)
async def create_task(message: Message, state: FSMContext):
    try:
        date = date_formater(message.text)
    except:
        await message.answer("Неверный формат даты")
        return
    await state.update_data(task_status="active")
    await state.update_data(task_time_limit=str(date))
    await state.update_data(task_checker_id=message.from_user.id)
    info = await state.get_data()
    add_task(info['task_name'], info['task_description'],
             info['task_status'], info['task_time_limit'], info['task_checker_id'])
    os.mkdir(f"files/{info['task_name']}")
    os.mkdir(f"files/{info['task_name']}/obsh_ams")
    os.mkdir(f"files/{info['task_name']}/up_ams")
    os.mkdir(f"files/{info['task_name']}/down_ams")
    os.mkdir(f"files/{info['task_name']}/crop_ams")
    os.mkdir(f"files/{info['task_name']}/shadow_ams")
    os.mkdir(f"files/{info['task_name']}/connect_ams")
    await message.answer(f"Задание создано")
    await state.clear()


# TODO: функция в бд для возвращения всех своих задач
@admin_router.message(F.text == "Добавить исполнителя")
async def add_executor(message: Message, state: FSMContext):
    await message.answer("Выберете задание для добавления исполнителя", reply_markup=task_preview_keyboard(message.from_user.id))
    await state.set_state(Admin.WAITING_FOR_TASK_ID)


@admin_router.callback_query(Admin.WAITING_FOR_TASK_ID)
async def get_task_id(query, state: FSMContext):
    await state.update_data(task_id=query.data)
    await query.message.edit_text(f"Перешлите сообщение от исполнителя")
    await state.set_state(Admin.WAITING_FOR_ADD_EXECUTOR)


@admin_router.message(Admin.WAITING_FOR_ADD_EXECUTOR)
async def add_executor_id(message: Message, state: FSMContext):
    info = await state.get_data()
    add_task_worker(info['task_id'], 'worker_list',
                    '{' + f'{message.forward_from.id}' + '}')
    await state.clear()


@admin_router.message(F.text == "Проверить задания")
async def get_task_to_check(message: Message, state: FSMContext):
    await message.answer("Все файлы лежат в папке files/название задания/название этапа/название файла")
    await state.set_state(Admin.WAITING_FOR_REVIEW)
    await state.clear()
