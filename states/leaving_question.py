from aiogram.fsm.state import StatesGroup, State


class LeaveQuestion(StatesGroup):
    user_id = ""
    type = 0
    question = State()
    tags = State()
