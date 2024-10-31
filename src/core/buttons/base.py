from typing import ClassVar

from pydantic import BaseModel, ConfigDict
from aiogram.filters.callback_data import CallbackData


class Button(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    callback_data: CallbackData | str | None = None


class ButtonGroup(BaseModel):
    model_config = ConfigDict(frozen=True)

    rows: ClassVar = ()
