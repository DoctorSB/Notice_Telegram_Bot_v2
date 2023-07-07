from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def register_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать диалог"),
        BotCommand(command="/create_task", description="Создать задание"),
        BotCommand(command="/add_executor",
                   description="Добавить исполнителя к заданию"),
        BotCommand(command="/get_task", description="Получить задание"),
        BotCommand(command="/my_tasks", description="Получить мои задания")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
