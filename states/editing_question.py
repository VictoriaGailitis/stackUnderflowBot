from aiogram.fsm.state import StatesGroup, State


class EditQuestion(StatesGroup):
    question_id = 0
    user_id = ""
    type = 0
    question = State()
    tags = State()
