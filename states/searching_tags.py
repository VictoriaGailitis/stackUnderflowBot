from aiogram.fsm.state import StatesGroup, State


class SearchTag(StatesGroup):
    tags = State()
