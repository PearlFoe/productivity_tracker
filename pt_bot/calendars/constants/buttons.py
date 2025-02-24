from typing import ClassVar

from pt_bot.core.buttons.base import Button, ButtonGroup

from .callback_data import CalendarCategory, MenuAction


class MenuButtons(ButtonGroup):
    ADD_CALENDAR: ClassVar = Button(text="Add new calendar", callback_data=MenuAction.ADD_CALENDAR)
    DISABLE_CALENDAR: ClassVar = Button(text="Disable calendar", callback_data=MenuAction.DIABLE_CALENDAR)

    rows: ClassVar = (ADD_CALENDAR, DISABLE_CALENDAR)


class CategoryButtons(ButtonGroup):
    WORK: ClassVar = Button(text="work", callback_data=CalendarCategory.WORK)
    ENTERTAINMENT: ClassVar = Button(text="entertainment", callback_data=CalendarCategory.ENTERTAINMENT)

    rows: ClassVar = ((WORK, ENTERTAINMENT),)
