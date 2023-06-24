from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter
from tgbot.misc.json_work import remove_json, append_json, task_create
from tgbot.misc.states import Admin

from tgbot.models.quest import Quest
from tgbot.models.checker import Checker

admin_router = Router()
admin_router.message.filter(AdminFilter())
quest = Quest()
checker = Checker()


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Админка!")


@admin_router.message(Command(commands="set_checker"))
async def set_checker(message: Message, state: FSMContext):
    await state.set_state(Admin.WAITING_FOR_ADD_CHECKER)
    await message.answer("Введите id пользователя, которого хотите сделать проверяющим")


@admin_router.message(Admin.WAITING_FOR_ADD_CHECKER)
async def set_checker(message: Message, state: FSMContext):
    checker.set_id(message.text)
    append_json('data.json', 'checkers', checker.get_id())
    await state.clear()
    await message.answer("Вы сделали пользователя проверяющим")


@admin_router.message(Command(commands="remove_checker"))
async def remove_checker(message: Message, state: FSMContext):
    await state.set_state(Admin.WAITING_FOR_REMOVE_CHECKER)
    await message.answer("Введите id пользователя, которого хотите сделать проверяющим")


@admin_router.message(Admin.WAITING_FOR_REMOVE_CHECKER)
async def remove_checker(message: Message, state: FSMContext):
    remove_json('data.json', 'checkers', message.text)
    await state.clear()
    await message.answer("Вы удалили пользователя из проверяющих")


@admin_router.message(Command(commands="create_task"))
async def create_task(message: Message, state: FSMContext):
    await state.set_state(Admin.WAITING_FOR_TASK_NAME)
    await message.answer("Введите название задания")


@admin_router.message(Admin.WAITING_FOR_TASK_NAME)
async def create_task(message: Message, state: FSMContext):
    quest.set_quest_name(message.text)
    await message.answer("Введите описание задания")
    await state.set_state(Admin.WAITING_FOR_TASK_DESCRIPTION)


@admin_router.message(Admin.WAITING_FOR_TASK_DESCRIPTION)
async def create_task(message: Message, state: FSMContext):
    quest.set_quest_description(message.text)
    await message.answer("Введите время на выполнение задания в формате ДД.ММ.ГГГГ ЧЧ:ММ")
    await state.set_state(Admin.WAITING_FOR_TASK_TIME_LIMIT)


@admin_router.message(Admin.WAITING_FOR_TASK_TIME_LIMIT)
async def create_task(message: Message, state: FSMContext):
    quest.set_time_limit(message.text)
    await state.clear()
    task_create(quest)
    await message.answer(f"Задание создано {quest.get_quest_name()}\n{quest.get_quest_description()}\n{quest.get_time_limit()}")


@admin_router.message(Command(commands="add_executor"))
async def add_executor(message: Message, state: FSMContext):
    await state.set_state(Admin.WAITING_FOR_ADD_EXECUTOR)
    await message.answer("Введите id пользователя, которого хотите добавить в исполнители")
    quest.add_worker_id(message.text)
    await state.clear()
