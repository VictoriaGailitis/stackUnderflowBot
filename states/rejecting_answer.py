from aiogram.fsm.state import StatesGroup, State


class RejectAnswer(StatesGroup):
    answer_id = ""
    reason = State()
