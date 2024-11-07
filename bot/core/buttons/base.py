from typing import ClassVar

from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel, ConfigDict


class Button(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    callback_data: CallbackData | str | None = None


class ButtonGroup(BaseModel):
    model_config = ConfigDict(frozen=True)

    rows: ClassVar = ()
