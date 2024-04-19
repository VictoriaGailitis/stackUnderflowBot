from aiogram.fsm.state import StatesGroup, State


class RateAnswer(StatesGroup):
    answer_id = ""
    rating = State()
