from aiogram.fsm.state import StatesGroup, State


class LoginAdmin(StatesGroup):
    login = State()
    password = State()
