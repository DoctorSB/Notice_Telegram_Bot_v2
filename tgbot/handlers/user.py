from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from docx import Document
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.misc.states import User
from tgbot.database.db import add_task, add_task_files, add_task_worker, get_array_len, get_array_values, get_task_data, get_task_names_by_worker_id, update_task_status, update_task_worker_list

from tgbot.keyboards.reply import next_back_generator
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
    for name in tasks:
        text = get_task_data(name)
        data_string = text[0][1:-1]
        values = [value.strip('"') for value in data_string.split(',')]
        mes_text = f"Название: {name}\n" \
            f"Дата: {values[5]}\n" \
            f"Статус: {values[4]}\n" \
            f"Файлы: {values[3]}"

        await query.message.answer(mes_text, reply_markup=task_keyboard)
        await state.update_data(task_name=query.data)


@user_router.callback_query(User.ACCEPT_OR_CANCEL)
async def cancel_task(query, state: FSMContext):
    if query.data == "cancel":
        await query.message.edit_text(f"Вот список заданий:", reply_markup=task_preview_keyboard(query.from_user.id))
        await state.set_state(User.WAITING_FOR_TASK_NAME)
    if query.data == "accept":
        info = await state.get_data()
        await query.message.edit_text(f"Задание принято")
        add_task_worker(info['task_name'], info['user_id'])


@user_router.message(User.SEND_FILE)
async def append_file(message: Message, state: FSMContext):
    faze = await state.get_data()
    if faze['step'] == 'ams_files':
        print(1)
        text = ams
    if faze['step'] == 'apparat_files':
        print(2)
        text = apparatus
    if faze['step'] == 'afy_files':
        print(3)
        text = afy
    if faze['step'] == 'materials_files':
        print(4)
        text = 'materials'
    if message.photo:
        photo = message.photo[-1]
        add_task_files(faze['task_name'], faze['step'],
                       '{' + f'{photo.file_id}' + '}')
    if message.text == 'Завершить':
        await state.set_state(User.WAITING_FOR_TASK_NAME)
        await message.answer(f"Вот список заданий:", reply_markup=task_preview_keyboard(message.from_user.id))
    elif message.text == 'Назад':
        
        keyboard, new_step = next_back_generator(faze['step'], 1)
        await message.answer(text, reply_markup=keyboard)
        await state.update_data(step=new_step)

    elif message.text == 'Далее':
        
        keyboard, new_step = next_back_generator(faze['step'], 0)
        await message.answer(text, reply_markup=keyboard)
        await state.update_data(step=new_step)


@user_router.message(Command(commands="my_tasks"))
async def get_my_tasks(message: Message, state: FSMContext):
    for name in get_task_names_by_worker_id(message.from_user.id):
        text = get_task_data(name)
        data_string = text[0][1:-1]
        values = [value.strip('"') for value in data_string.split(',')]
        mes_text = f"Название: {name}\n" \
            f"Дата: {values[5]}\n" \
            f"Статус: {values[4]}\n" \
            f"Файлы: {values[3]}"
        await message.answer(mes_text, reply_markup=task_work)
        await state.update_data(task_name=name)
        await state.set_state(User.CHOOSE_TASK)


@user_router.callback_query(User.CHOOSE_TASK)
async def choose_task(query, state: FSMContext):
    if query.data == "add_files":
        await state.set_state(User.SEND_FILE)
        await state.update_data(step='ams_files')
        await query.message.edit_text(ams)
    if query.data == "send_to_check":
        await query.message.edit_text(f"Задание отправлено на проверку")
        status = "waiting"
        info = await state.get_data()
        update_task_status(info['task_name'], status)
        await state.finish()  # type: ignore
