# состояния
from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    GET_ROLE = State()
    WAITING_FOR_TASK_NAME = State()
    ACCEPT_OR_CANCEL = State()
    WAIT_SEND_FILE = State()
    CHOOSE_TASK = State()
    SEND_FILE_MENU = State()
    SEND_FILE = State()


class Admin(StatesGroup):
    WAITING_FOR_TASK_NAME = State()
    WAITING_FOR_TASK_DESCRIPTION = State()
    WAITING_FOR_TASK_TIME_LIMIT = State()
    WAITING_FOR_ADD_EXECUTOR = State()
    WAITING_FOR_TASK_ID = State()
    WAITING_FOR_CHECK_TASK = State()
