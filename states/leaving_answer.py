from aiogram.fsm.state import StatesGroup, State


class LeaveAnswer(StatesGroup):
    user_id = ""
    question_id = ""
    type = 0
    answer = State()
