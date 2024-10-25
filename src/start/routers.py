from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from .fsm import StartState
from .constants.messages import StartMessages

router = Router()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=StartMessages.START)
    await state.set_state(StartState.START)
