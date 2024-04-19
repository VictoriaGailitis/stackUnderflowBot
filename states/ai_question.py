from aiogram.fsm.state import StatesGroup, State


class AIQuestion(StatesGroup):
    cur_question = ""
    text = ""
    theme = State()
    tags = State()
