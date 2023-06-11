from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from docx import Document
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.misc.states import User
from tgbot.misc.json_work import json_add, json_read, json_write, remove_json, append_json

user_router = Router()

@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Привет")


@user_router.message(Command(commands="get_task"))
async def get_task(message: Message, state: FSMContext):
    tasks = json_read('tasks.json', 'tasks')
    await message.answer(f"Вот список заданий: {tasks}")
    await state.set_state(User.WAITING_FOR_TASK_NAME)
    await message.answer("Введите название задания")


