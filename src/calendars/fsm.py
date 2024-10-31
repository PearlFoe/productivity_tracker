from aiogram.fsm.state import StatesGroup, State


class CalendarState(StatesGroup):
    LINK = State()
    CATEGORY = State()
