from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def register_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать диалог"),
        BotCommand(command="/set_checker",
                   description="Добавить проверяющего"),
        BotCommand(command="/remove_checker",
                   description="Удалить проверяющего"),
        BotCommand(command="/create_task", description="Создать задание"),
        BotCommand(command="/set_task_description",
                   description="Задать описание задания"),
        BotCommand(command="/add_photo",
                   description="Добавить фото к заданию"),
        BotCommand(command="/add_executor",
                   description="Добавить исполнителя к заданию"),
        BotCommand(command="/finish_task", description="Завершить задание"),
        BotCommand(command="/get_task", description="Получить задание"),
        BotCommand(command="/my_tasks", description="Получить мои задания")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
