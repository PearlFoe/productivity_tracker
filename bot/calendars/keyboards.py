from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.buttons.base import ButtonGroup
from bot.core.keyboards import BaseKeyboard

from .constants import buttons


class CalendarKeyboard(BaseKeyboard):
    @classmethod
    def category_kb(
        cls: type["CalendarKeyboard"],
        buttons_group: ButtonGroup = buttons.CategoryButtons,
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        cls._add_buttons(builder, buttons_group, InlineKeyboardButton)
        return builder.as_markup()
