from aiogram.fsm.state import State, StatesGroup


class Posting(StatesGroup):
    time = State()
    message = State()
