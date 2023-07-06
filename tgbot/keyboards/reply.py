from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def next_back_generator(step, back):
    if step == 'ams_files':
        step = 'apparat_files'
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Далее")
                ]
            ],
            resize_keyboard=True
        ), step
    if step == 'apparat_files':
        if back == 1:
            step = 'ams_files'
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Далее"),
                    ]
                ],
                resize_keyboard=True
            ), step
        step = 'afy_files'
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Далее"),
                    KeyboardButton(text="Назад")
                ]
            ],
            resize_keyboard=True
        ), step
    if step == 'afy_files':
        if back == 1:
            step = 'apparat_files'
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Далее"),
                        KeyboardButton(text="Назад")
                    ]
                ],
                resize_keyboard=True
            ), step
        step = 'materials_files'
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Далее"),
                    KeyboardButton(text="Назад")
                ]
            ],
            resize_keyboard=True
        ), step
    if step == 'materials_files':
        if back == 1:
            step = 'afy_files'
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Далее"),
                        KeyboardButton(text="Назад")
                    ]
                ],
                resize_keyboard=True
            ), step
        step = 'materials_files'
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Завершить"),
                    KeyboardButton(text="Назад")

                ]
            ],
            resize_keyboard=True
        ), step
