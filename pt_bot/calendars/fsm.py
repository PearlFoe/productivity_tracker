from aiogram.fsm.state import State, StatesGroup


class CalendarState(StatesGroup):
    CHOOSE_ACTION = State()
    PROCESS_LINK = State()
    SET_CATEGORY = State()
    CHOOSE_NAME = State()
