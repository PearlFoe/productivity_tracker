from typing import ClassVar

from src.core.buttons.base import Button, ButtonGroup


class CategoryButtons(ButtonGroup):
    WORK: ClassVar = Button("work", callback_data="WORK")
    ENTERTAINMENT: ClassVar = Button("entertainment", callback_data="ENTERTAINMENT")

    rows: ClassVar = ((WORK, ENTERTAINMENT),)
