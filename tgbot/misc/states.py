# состояния
from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    GET_ROLE = State()
    WAITING_FOR_TASK_NAME = State()
    ACCEPT_OR_CANCEL = State()
    WORK_ON_TASK = State()


class Admin(StatesGroup):
    WAITING_FOR_ADD_CHECKER = State()
    WAITING_FOR_REMOVE_CHECKER = State()
    WAITING_FOR_TASK_NAME = State()
    WAITING_FOR_TASK_DESCRIPTION = State()
    WAITING_FOR_TASK_TIME_LIMIT = State()
    WAITING_FOR_ADD_EXECUTOR = State()
