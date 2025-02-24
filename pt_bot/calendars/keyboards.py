from collections.abc import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from pt_bot.core.buttons.base import Button, ButtonGroup
from pt_bot.core.keyboards import BaseKeyboard

from .constants import buttons


class CalendarKeyboard(BaseKeyboard):
    @classmethod
    def menu_kb(
        cls: type["CalendarKeyboard"],
        buttons_group: ButtonGroup = buttons.MenuButtons,
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        cls._add_buttons(builder, buttons_group, InlineKeyboardButton)
        return builder.as_markup()

    @classmethod
    def category_kb(
        cls: type["CalendarKeyboard"],
        buttons_group: ButtonGroup = buttons.CategoryButtons,
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        cls._add_buttons(builder, buttons_group, InlineKeyboardButton)
        return builder.as_markup()

    @classmethod
    def disable_calendar_kb(
        cls: type["CalendarKeyboard"],
        buttons_group: Iterable[Button],
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        cls._add_buttons(builder, buttons_group, InlineKeyboardButton)
        return builder.as_markup()
