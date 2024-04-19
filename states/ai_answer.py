from aiogram.fsm.state import StatesGroup, State


class AIAnswer(StatesGroup):
    cur_answer = ""
    text = ""
    theme = State()
