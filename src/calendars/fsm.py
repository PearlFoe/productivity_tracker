from aiogram.fsm.state import State, StatesGroup


class CalendarState(StatesGroup):
    LINK = State()
    CATEGORY = State()
