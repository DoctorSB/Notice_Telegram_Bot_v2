from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import Bot


from tgbot.misc.states import User
from tgbot.config import load_config
from tgbot.database.db import add_task_files, add_task_worker, get_task_data, get_task_names_by_worker_id, update_task_status, get_task_where_menya_net

from tgbot.keyboards.reply import next_back_generator, main_keyboard, cancel_keyboard
from tgbot.keyboards.inline import task_keyboard, task_preview_keyboard, task_work, active_tasks_keyboard
from tgbot.text.shablons import ams_files, afy_files, apparat_files, materials_files

user_router = Router()

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext):
    await message.reply("Вы исполнитель", reply_markup=main_keyboard)
    await state.clear()


@user_router.message(F.text == 'Отмена')
async def cancel(message: Message, state: FSMContext):
    await message.answer(f"Вы в главном меню", reply_markup=main_keyboard)
    await state.clear()


@user_router.message(F.text == 'Получить задание')
async def get_task(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await message.answer(f"Вот список заданий:", reply_markup=active_tasks_keyboard(message.from_user.id))
    await state.set_state(User.WAITING_FOR_TASK_NAME)


@user_router.callback_query(User.WAITING_FOR_TASK_NAME)
async def get_task_info(query, state: FSMContext):
    await state.update_data(task_name=query.data)
    text = get_task_data(query.data)
    data_string = text[0][1:-1]
    values = [value.strip('"') for value in data_string.split(',')]
    mes_text = f"Название: {query.data}\n" \
        f"Описание: {values[0]}\n" \
        f"Дата: {values[7]}\n" \
        f"Статус: {values[6]}\n" \
        f"Проверяющий: {values[9]}"
    await query.message.edit_text(mes_text, reply_markup=task_keyboard) 
    
    await state.set_state(User.ACCEPT_OR_CANCEL)
    


@user_router.callback_query(User.ACCEPT_OR_CANCEL)
async def cancel_task(query, state: FSMContext):
    if query.data == "cancel":
        await query.message.edit_text(f"Вот список заданий:", reply_markup=task_preview_keyboard(query.from_user.id))
        await state.set_state(User.WAITING_FOR_TASK_NAME)
    if query.data == "accept":
        info = await state.get_data()
        await query.message.edit_text(f"Задание принято")
        add_task_worker(info['task_name'], 'worker_list', '{' + str(info['user_id']) + '}')


@user_router.message(F.text == 'Мои задания')
async def get_my_tasks(message: Message, state: FSMContext):
    await message.answer(f"Вот список ваших заданий:", reply_markup=cancel_keyboard)
    for name in get_task_names_by_worker_id(message.from_user.id):
        text = get_task_data(name)
        data_string = text[0][1:-1]
        values = [value.strip('"') for value in data_string.split(',')]
        mes_text = f"Название: {name}\n" \
            f"Дата: {values[7]}\n" \
            f"Статус: {values[6]}\n" \
            f"Проверяющий: {values[9]}"
        await message.answer(mes_text, reply_markup=task_work)
        await state.update_data(task_name=name)
    await state.set_state(User.CHOOSE_TASK)


@user_router.callback_query(User.CHOOSE_TASK)
async def choose_task(query, state: FSMContext, message: Message):
    if query.data == "add_files":
        await state.set_state(User.SEND_FILE)
        await state.update_data(step='ams_files')
        await query.message.edit_text(ams_files)
    if query.data == "send_to_check":
        await query.message.edit_text(f"Задание отправлено на проверку")
        status = "waiting"
        info = await state.get_data()
        update_task_status(info['task_name'], status)


@user_router.message(User.SEND_FILE)
async def append_file(message: Message, state: FSMContext):
    faze = await state.get_data()
    if message.photo:
        photo = message.photo[-1]
        await bot.download(file=photo, destination=f"files/{faze['task_name']}/{faze['step']}/{photo.file_id}.jpg")
        add_task_files(faze['task_name'], faze['step'],
                       '{' + f'{photo.file_id}' + '}')
    if message.text == 'Завершить':
        await message.answer(f"Задание отправлено на проверку")
        status = "waiting"
        info = await state.get_data()
        update_task_status(info['task_name'], status)
        await state.clear()
    elif message.text == 'Назад':
        keyboard, new_step = next_back_generator(faze['step'], 1)
        await message.answer(eval(new_step), reply_markup=keyboard)
        await state.update_data(step=new_step)
    elif message.text == 'Далее':
        keyboard, new_step = next_back_generator(faze['step'], 0)
        await message.answer(eval(new_step), reply_markup=keyboard)
        await state.update_data(step=new_step)
