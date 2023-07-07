from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.filters.admin import AdminFilter
from tgbot.database.db import add_task, get_task_by_name, add_task_worker, find_tasks_by_checker_and_status


from tgbot.misc.data_formater import date_formater
from tgbot.misc.states import Admin

from tgbot.keyboards.inline import task_preview_keyboard, tasks_for_review_keyboard, task_keyboard

from tgbot.models.quest import Quest
from tgbot.models.checker import Checker


admin_router = Router()
admin_router.message.filter(AdminFilter())
quest = Quest()
checker = Checker()


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Вы проверяющий", reply_markup=ReplyKeyboardRemove())


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


# TODO: функция в бд для возвращения всех своих задач
@admin_router.message(Command(commands="add_executor"))
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
    await message.answer("Выберете задание для проверки",)
    await state.set_state(Admin.WAITING_FOR_REVIEW)
    task = find_tasks_by_checker_and_status(message.from_user.id, "waiting")
    print(task)
    for mes in task:
        redy = mes[1:].split(',')
        await message.answer(f"Задание: {redy[0]}\nОписание: {redy[1]}\nВремя на выполнение: {redy[7]}\nИсполнитель: {redy[9]}", reply_markup=task_keyboard)
