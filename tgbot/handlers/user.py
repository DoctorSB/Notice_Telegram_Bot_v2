from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from docx import Document
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.misc.states import User
from tgbot.misc.json_work import json_read, output_all, task_output, json_add_worker
from tgbot.keyboards.inline import task_keyboard, task_preview_keyboard

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Привет")


@user_router.message(Command(commands="get_task"))
async def get_task(message: Message, state: FSMContext):
    state.update_data(user_id=message.from_user.id)
    await message.answer(f"Вот список заданий:", reply_markup=task_preview_keyboard('tasks.json'))
    await state.set_state(User.WAITING_FOR_TASK_NAME)


@user_router.callback_query(User.WAITING_FOR_TASK_NAME)
async def get_task_info(query, state: FSMContext):
    for key in json_read('tasks.json'):
        if key == query.data:
            text = task_output('tasks.json', query.data)
            state.update_data(task_name=query.data)
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
        await state.set_state(User.WORK_ON_TASK)