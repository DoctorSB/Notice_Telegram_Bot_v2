from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


values = {
    1: "ams_files",
    2: "apparat_files",
    3: "afy_files",
    4: "materials_files",
}


def next_back_generator(step, back):
    iterator = [1, 2, 3, 4]
    for i in iterator:
        if values[i] == step:
            if i == 1:
                buttons = [[KeyboardButton(text="Далее")]]
                i = 2
                return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True), values[i]
            
            if i == 2 and back == 1:
                buttons = [
                    [
                        KeyboardButton(text="Далее"),
                        KeyboardButton(text="Назад")
                    ]
                ]
                i = 1
                return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True), values[i]
            elif i == 2:
                buttons = [
                    [
                        KeyboardButton(text="Далее"),
                        KeyboardButton(text="Назад")
                    ]
                ]
                i = 3
                return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True), values[i]
            if i == 3 and back == 1:
                buttons = [
                    [
                        KeyboardButton(text="Далее"),
                        KeyboardButton(text="Назад")
                    ]
                ]
                i = 2
                return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True), values[i]
            elif i == 3:
                buttons = [
                    [
                        KeyboardButton(text="Завершить"),
                        KeyboardButton(text="Назад")
                    ]
                ]
                i = 4
                return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True), values[i]
            if i == 4 and back == 1:
                buttons = [
                    [
                        KeyboardButton(text="Далее"),
                        KeyboardButton(text="Назад")
                    ]
                ]
                i = 3
                return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True), values[i]
            elif i == 4:
                buttons = [
                    [
                        KeyboardButton(text="Завершить"),
                        KeyboardButton(text="Назад")
                    ]
                ]
            return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True), values[i]


if __name__ == '__main__':
    print(values[1])
