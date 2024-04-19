from aiogram.fsm.state import StatesGroup, State


class RejectQuestion(StatesGroup):
    question_id = ""
    reason = State()
