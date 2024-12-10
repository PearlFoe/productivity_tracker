from typing import ClassVar

from pt_bot.core.buttons.base import Button, ButtonGroup

from ..constants.calendar_category import CalendarCategory


class CategoryButtons(ButtonGroup):
    WORK: ClassVar = Button(text="work", callback_data=CalendarCategory.WORK)
    ENTERTAINMENT: ClassVar = Button(text="entertainment", callback_data=CalendarCategory.ENTERTAINMENT)

    rows: ClassVar = ((WORK, ENTERTAINMENT),)
