from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .constants import buttons
from src.core.keyboards import BaseKeyboard
from src.core.buttons.base import ButtonGroup


class CalendarKeyboard(BaseKeyboard):
    @classmethod
    def category_kb(
        cls: type["CalendarKeyboard"],
        buttons_group: ButtonGroup = buttons.CategoryButtons,
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        cls._add_buttons(builder, buttons_group, InlineKeyboardButton)
        return builder.as_markup()
