from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from docx import Document
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.misc.states import User
from tgbot.misc.json_work import json_read, task_output, json_add_worker, json_add_photo, json_write
from tgbot.keyboards.inline import task_keyboard, task_preview_keyboard, task_work

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Привет")


@user_router.message(Command(commands="get_task"))
async def get_task(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await message.answer(f"Вот список заданий:", reply_markup=task_preview_keyboard('tasks.json'))
    await state.set_state(User.WAITING_FOR_TASK_NAME)


@user_router.callback_query(User.WAITING_FOR_TASK_NAME)
async def get_task_info(query, state: FSMContext):
    for key in json_read('tasks.json'):
        if key == query.data:
            text = task_output('tasks.json', query.data)
            await state.update_data(task_name=query.data)
            await query.message.edit_text(text=text, reply_markup=task_keyboard)
            await state.set_state(User.ACCEPT_OR_CANCEL)


@user_router.callback_query(User.ACCEPT_OR_CANCEL)
async def cancel_task(query, state: FSMContext):
    if query.data == "cancel":
        await query.message.edit_text(f"Вот список заданий:", reply_markup=task_preview_keyboard('tasks.json'))
        await state.set_state(User.WAITING_FOR_TASK_NAME)
    if query.data == "accept":
        info = await state.get_data()
        await query.message.edit_text(f"Задание принято")
        json_add_worker('tasks.json', info['task_name'], info['user_id'])


@user_router.message(User.WORK_ON_TASK)
async def work_on_task(message: Message, state: FSMContext):
    await message.answer("Отправьте файлы для проверки")
    await state.set_state(User.SEND_FILE)


@user_router.message(User.SEND_FILE)
async def append_photo(message: Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1]
        json = json_read('tasks.json')
        info = await state.get_data()
        json_add_photo('tasks.json', info['task_name'], photo.file_id)
    if message.text == "Завершить":
        await message.answer("Задание завершено")
        status = "done"
        json = json_read('tasks.json')
        info = await state.get_data()
        json[info['task_name']]["status"] = status
        await state.finish()


@user_router.message(Command(commands="my_tasks"))
async def get_my_tasks(message: Message, state: FSMContext):
    for key in json_read('tasks.json'):
        if message.from_user.id in json_read('tasks.json')[key]["worker_list"]:
            text = task_output('tasks.json', key)
            await message.answer(text=text, reply_markup=task_work)
            await state.set_state(User.CHOOSE_TASK)

@user_router.callback_query(User.CHOOSE_TASK)
async def choose_task(query, state: FSMContext):
    if query.data == "add_files":
        await query.message.edit_text(f"Отправьте файлы для проверки")
        await state.set_state(User.SEND_FILE)
    if query.data == "send_to_check":
        await query.message.edit_text(f"Задание отправлено на проверку")
        status = "waiting"
        json = json_read('tasks.json')
        info = await state.get_data()
        json[info['task_name']]["status"] = status
        json_write('tasks.json', json)

#await state.set_state(User.WORK_ON_TASK)