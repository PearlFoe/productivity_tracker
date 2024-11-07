from typing import ClassVar

from bot.core.buttons.base import Button, ButtonGroup


class CategoryButtons(ButtonGroup):
    WORK: ClassVar = Button(text="work", callback_data="WORK")
    ENTERTAINMENT: ClassVar = Button(text="entertainment", callback_data="ENTERTAINMENT")

    rows: ClassVar = ((WORK, ENTERTAINMENT),)
