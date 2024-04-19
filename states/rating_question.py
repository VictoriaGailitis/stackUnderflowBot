from aiogram.fsm.state import StatesGroup, State


class RateQuestion(StatesGroup):
    question_id = ""
    rating = State()
