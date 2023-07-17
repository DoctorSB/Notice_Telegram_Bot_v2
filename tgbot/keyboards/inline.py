from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.database.db import get_task_names_by_worker_id, find_tasks_by_checker_and_status, get_task_where_menya_net, get_array_len, get_names_for_admin



accept_button = [[InlineKeyboardButton(text="Принять", callback_data="accept")],
                 [InlineKeyboardButton(text="Назад", callback_data="cancel")]]

task_keyboard = InlineKeyboardMarkup(inline_keyboard=accept_button)


def task_preview_keyboard(id):
    data = get_task_names_by_worker_id(id)
    keyboard = []
    for name in data:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=name)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def task_preview_keyboard_for_admin():
    data = get_names_for_admin()
    keyboard = []
    for name in data:
        new_name = name[0]
        keyboard.append([InlineKeyboardButton(text=new_name, callback_data=new_name)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)




def active_tasks_keyboard(id):
    data = get_task_where_menya_net(id)
    keyboard = []
    for name in data:
        new_name = name[0]
        keyboard.append([InlineKeyboardButton(text=new_name, callback_data=new_name)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


task_button = [[InlineKeyboardButton(text="Добавить файлы", callback_data="add_files")],
               [InlineKeyboardButton(text="Отправить на проверку", callback_data="send_to_check")]]

task_work = InlineKeyboardMarkup(inline_keyboard=task_button)


def tasks_for_review_keyboard(id):
    data = find_tasks_by_checker_and_status(id, "waiting")
    keyboard = []
    for name in data:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=name)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def photo_send_puncts_button_geberator(task):
    ams_puncts_dict = {
        'obsh_ams': 6,
        'up_ams': 6,
        'down_ams': 6,
        'crop_ams': 6,
        'shadow_ams': 12,
        'connect_ams': 4
    }
    apparat_punct_dict = {
        'outdoor_app': 4,
        'oborud_app': 4,
        'block_app': 4,
        'automat_app': 4,
        'cabel_app': 4,
        'pribor_app': 4,
        'trace_app': 4
    }
    afy_punct_dict = {
        'antenna_afy': 18,
        'mehan_afy': 12,
        'sticker_afu': 1,
        'azimuth_afy': 4,
        'outlook_afy': 6,
        'block_afy': 12,
        'cabel_afy': 6,
    }
    materials_punct_dict = {
        'gps_display': 1,
    }
    ams_puncts_list = ['Общий вид амс в полный', 'Верхняя часть AMC', 'Нижняя часть AMC', 'Bce опорные фланцы крупным планом', 'Фото скрытых работ', 'Место соединения троса']
    apparat_punct_list = ['Стойка Outdoor', 'Оборудование', ' РРЛ/мультиплексор/модем', 'Автоматы подключения', 'Кабельный ввод', 'Прибор учета', 'Трасса прокладки кабеля']
    afy_punct_list = ['Азимуты антенн БС', 'Механические углы', 'Фото наклейки', 'Азимуты антенн РРЛ', 'Общий вид здания', 'Внешние блоки', 'Кабельная трасса']
    materials_punct_list = ['Дисплей GPS']
    keyboard = []
    count = 0
    for i in ams_puncts_dict.keys():
        if get_array_len(task, i) is None:
            photos_count = 0
        else:
            photos_count = get_array_len(task, i)
        if photos_count >= ams_puncts_dict[i]:
            keyboard.append([InlineKeyboardButton(text=f'{ams_puncts_list[count]} ✅', callback_data=i)])
        else:
            keyboard.append([InlineKeyboardButton(text=f'{ams_puncts_list[count]} ({get_array_len(task, i)}/{ams_puncts_dict[i]})', callback_data=i)])
        count += 1
    count = 0
    for i in apparat_punct_dict.keys():
        if get_array_len(task, i) is None:
            photos_count = 0
        else:
            photos_count = get_array_len(task, i)
        if photos_count >= apparat_punct_dict[i]:
            keyboard.append([InlineKeyboardButton(text=f'{apparat_punct_list[count]} ✅', callback_data=i)])
        else:
            keyboard.append([InlineKeyboardButton(text=f'{apparat_punct_list[count]} ({get_array_len(task, i)}/{apparat_punct_dict[i]})', callback_data=i)])
        count += 1
    count = 0
    for i in afy_punct_dict.keys():
        if get_array_len(task, i) is None:
            photos_count = 0
        else:
            photos_count = get_array_len(task, i)
        if photos_count >= afy_punct_dict[i]:
            keyboard.append([InlineKeyboardButton(text=f'{afy_punct_list[count]} ✅', callback_data=i)])
        else:
            keyboard.append([InlineKeyboardButton(text=f'{afy_punct_list[count]} ({get_array_len(task, i)}/{afy_punct_dict[i]})', callback_data=i)])
        count += 1
    count = 0
    for i in materials_punct_dict.keys():
        if get_array_len(task, i) is None:
            photos_count = 0
        else:
            photos_count = get_array_len(task, i)
        if photos_count >= materials_punct_dict[i]:
            keyboard.append([InlineKeyboardButton(text=f'{materials_punct_list[count]} ✅', callback_data=i)])
        else:
            keyboard.append([InlineKeyboardButton(text=f'{materials_punct_list[count]} ({get_array_len(task, i)}/{materials_punct_dict[i]})', callback_data=i)])
        count += 1
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="cancel")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

