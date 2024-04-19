from aiogram.fsm.state import StatesGroup, State


class SubscribeTag(StatesGroup):
    user_id = 0
    tags = State()
    time = State()