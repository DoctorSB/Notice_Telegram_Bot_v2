from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_buttons = [
    [
        KeyboardButton(text="Получить задание"),
        KeyboardButton(text="Мои задания")
    ],
]

main_keyboard = ReplyKeyboardMarkup(
    keyboard=main_buttons, resize_keyboard=True)


admin_buttons = [
    [
        KeyboardButton(text="Создать задание"),
    ],
    [
        KeyboardButton(text="Добавить исполнителя"),
    ],
    [
        KeyboardButton(text="Проверить задание")
    ],
    [
        KeyboardButton(text="Список заданий")
    ]
]

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=admin_buttons, resize_keyboard=True)


cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отмена")]], resize_keyboard=True)
