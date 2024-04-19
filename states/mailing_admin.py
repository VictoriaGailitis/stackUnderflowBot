from aiogram.fsm.state import StatesGroup, State


class MailAdmin(StatesGroup):
    text = State()
    timedate = State()
