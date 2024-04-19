from aiogram.fsm.state import StatesGroup, State


class EditAnswer(StatesGroup):
    answer_id = 0
    user_id = ""
    question_id = ""
    type = 0
    answer = State()
