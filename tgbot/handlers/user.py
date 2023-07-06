from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from docx import Document
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.misc.states import User
from tgbot.database.db import add_task, add_task_files, add_task_worker, get_array_len, get_array_values, get_task_data, get_task_names_by_worker_id, update_task_status, update_task_worker_list

from tgbot.keyboards.inline import task_keyboard, task_preview_keyboard, task_work
from tgbot.text.shablons import ams, apparatus, afy

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Привет")


@user_router.message(Command(commands="get_task"))
async def get_task(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await message.answer(f"Вот список заданий:", reply_markup=task_preview_keyboard(message.from_user.id))
    await state.set_state(User.WAITING_FOR_TASK_NAME)


@user_router.callback_query(User.WAITING_FOR_TASK_NAME)
async def get_task_info(query, state: FSMContext):
    tasks = get_task_names_by_worker_id(query.from_user.id)
    if query.data in tasks:
        pass



@user_router.callback_query(User.ACCEPT_OR_CANCEL)
async def cancel_task(query, state: FSMContext):
    if query.data == "cancel":
        await query.message.edit_text(f"Вот список заданий:", reply_markup=task_preview_keyboard(query.from_user.id))
        await state.set_state(User.WAITING_FOR_TASK_NAME)
    if query.data == "accept":
        info = await state.get_data()
        await query.message.edit_text(f"Задание принято")
        add_task_worker(info['task_name'], info['user_id'])


@user_router.message(User.WORK_ON_TASK_AMS)
async def work_on_task_ams(message: Message, state: FSMContext):
    await message.answer(apparatus)
    await state.set_state(User.SEND_FILE_AMS)

@user_router.message(User.WORK_ON_TASK_APPARATUS)
async def work_on_task_apparatus(message: Message, state: FSMContext):
    await message.answer(afy)
    await state.set_state(User.SEND_FILE_AMS)


@user_router.message(User.SEND_FILE_AMS)
async def append_photo(message: Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1]
        info = await state.get_data()
        add_task_files(info['task_name'], photo.file_id)
    if message.text == "Завершить":
        await message.answer("Задание завершено")
        status = "Completed"
        info = await state.get_data()
        update_task_status(info['task_name'], status)
        await state.finish() # type: ignore


@user_router.message(Command(commands="my_tasks"))
async def get_my_tasks(message: Message, state: FSMContext):
    for name in get_task_names_by_worker_id(message.from_user.id):
        data = get_task_data(name)
        await message.answer(f"Название: {name}\n"
                             f"Дата: {data['date']}\n"
                             f"Статус: {data['status']}\n"
                             f"Файлы: {data['files']}")
        await message.answer(f"Задание принято", reply_markup=task_work)
        await state.update_data(task_name=name)
        await state.set_state(User.CHOOSE_TASK)


@user_router.callback_query(User.CHOOSE_TASK)
async def choose_task(query, state: FSMContext):
    if query.data == "add_files":
        await query.message.edit_text(ams)
        await state.set_state(User.SEND_FILE_AMS)
    if query.data == "send_to_check":
        await query.message.edit_text(f"Задание отправлено на проверку")
        status = "waiting"
        info = await state.get_data()
        update_task_status(info['task_name'], status)
        await state.finish() # type: ignore

