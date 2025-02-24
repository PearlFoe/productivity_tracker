from enum import StrEnum, auto


class MenuAction(StrEnum):
    ADD_CALENDAR = auto()
    DIABLE_CALENDAR = auto()


class CalendarCategory(StrEnum):
    WORK = auto()
    ENTERTAINMENT = auto()
