from collections.abc import Iterable

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ButtonType, KeyboardBuilder

from .buttons.base import Button, ButtonGroup


class BaseKeyboard:
    @staticmethod
    def __add_row(
        builder: KeyboardBuilder,
        button_type: type[ButtonType],
        row: tuple[Button] | Button,
    ) -> None:
        if isinstance(row, tuple):
            builder.row(
                *[
                    button_type(
                        text=button.text,
                        callback_data=button.callback_data.pack()
                        if isinstance(button.callback_data, CallbackData)
                        else button.callback_data,
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
                    else row.callback_data,
                )
            )

    @classmethod
    def _add_buttons(
        cls: type["BaseKeyboard"],
        builder: KeyboardBuilder,
        buttons: type[ButtonGroup] | Iterable[Button],
        button_type: type[ButtonType],
    ) -> None:
        rows = buttons if isinstance(buttons, Iterable) else buttons.rows
        for row in rows:
            cls.__add_row(builder, button_type, row)
