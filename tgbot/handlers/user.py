from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from docx import Document
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.misc.states import User
from tgbot.misc.json_work import json_read, output_all, task_output
from tgbot.keyboards.inline import task_keyboard, task_preview_keyboard

user_router = Router()

@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Привет")


@user_router.message(Command(commands="get_task"))
async def get_task(message: Message, state: FSMContext):
    text = output_all('tasks.json')
    await message.answer(f"Вот список заданий:", reply_markup=task_preview_keyboard('tasks.json'))
    await state.set_state(User.WAITING_FOR_TASK_NAME)
    await message.answer("Введите название задания")

@user_router.callback_query(User.WAITING_FOR_TASK_NAME)
async def get_task(query, state: FSMContext):
    for key in json_read('tasks.json'):
        if key == query.data:
            text = task_output('tasks.json', query.data)
            await query.message.edit_text(text=text, reply_markup=task_keyboard)
            await state.clear()
            