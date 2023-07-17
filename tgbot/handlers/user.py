from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import Bot


from tgbot.misc.states import User
from tgbot.config import load_config
from tgbot.database.db import add_task_files, add_task_worker, update_task_status

from tgbot.keyboards.reply import main_keyboard
from tgbot.keyboards.inline import task_keyboard, task_preview_keyboard, active_tasks_keyboard, photo_send_puncts_button_geberator

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
    mes_text = f"Название: {query.data}"
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
        add_task_worker(info['task_name'], 'worker_list',
                        '{' + str(info['user_id']) + '}')


@user_router.message(F.text == 'Мои задания')
async def get_my_tasks(message: Message, state: FSMContext):
    await message.answer(f"Вот список ваших заданий:", reply_markup=task_preview_keyboard(message.from_user.id))
    await state.set_state(User.CHOOSE_TASK)


@user_router.callback_query(User.CHOOSE_TASK)
async def choose_task(query, state: FSMContext):
    await query.message.edit_text(f'{query.data}', reply_markup=photo_send_puncts_button_geberator(query.data))
    await state.update_data(task_name=query.data)
    await state.set_state(User.SEND_FILE_MENU)


@user_router.callback_query(User.SEND_FILE_MENU)
async def send_file_menu(query, state: FSMContext):
    info = await state.get_data()
    if query.data == "cancel":
        await query.message.edit_text(f'{info["task_name"]}', reply_markup=task_preview_keyboard(query.from_user.id))
        await state.set_state(User.CHOOSE_TASK)
    else:
        await state.update_data(step=query.data)
        await query.message.edit_text(f"Отправьте фото для {query.data}")
        await state.set_state(User.SEND_FILE)


@user_router.message(User.SEND_FILE)
async def append_file(message: Message, state: FSMContext):
    await state.update_data(count=0)
    faze = await state.get_data()
    if message.photo and faze['count'] <= 2:
        photo = message.photo[-1]
        await bot.download(file=photo, destination=f"files/{faze['task_name']}/{faze['step']}/{photo.file_id}.jpg")
        add_task_files(faze['task_name'], faze['step'],
                       '{' + f'{photo.file_id}' + '}')
    if message.text == 'Завершить' or faze['count'] >= 2:
        await message.answer(f"Задание отправлено на проверку")
        status = "waiting"
        info = await state.get_data()
        update_task_status(info['task_name'], status)
        await state.clear()
