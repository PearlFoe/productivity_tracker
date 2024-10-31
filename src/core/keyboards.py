from collections.abc import Iterable

from aiogram.utils.keyboard import KeyboardBuilder, ButtonType
from aiogram.filters.callback_data import CallbackData

from .buttons.base import ButtonGroup, Button


class BaseKeyboard:
    @staticmethod
    def _add_row(
        builder: KeyboardBuilder,
        button_type: type[ButtonType],
        row: tuple[Button] | Button
    ) -> None:
        if isinstance(row, tuple):
            builder.row(
                *[
                    button_type(
                        text=button.text,
                        callback_data=button.callback_data.pack()
                            if isinstance(button.callback_data, CallbackData)
                            else button.callback_data
                    )
                    for button in row
                ]
            )
        else:
            builder.row(
                button_type(
                    text=row.text,
                    callback_data=row.callback_data.pack()
                        if isinstance(row.callback_data, CallbackData)
                        else row.callback_data
                    )
            )

    @classmethod
    def add_buttons(
        cls: type["BaseKeyboard"],
        builder: KeyboardBuilder,
        buttons: type[ButtonGroup] | Iterable[Button],
        button_type: type[ButtonType]
    ) -> None:
        rows = buttons if isinstance(buttons, Iterable) else buttons.rows
        for row in rows:
            cls._add_row(builder, button_type, row)
