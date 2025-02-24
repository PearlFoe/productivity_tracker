from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from ..constants.messages import CalendarMessages
from ..fsm import CalendarState
from ..keyboards import CalendarKeyboard

router = Router()


@router.message(Command("calendar"))
async def show_menu(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=CalendarMessages.MENU, reply_markup=CalendarKeyboard.menu_kb())
    await state.set_state(CalendarState.CHOOSE_ACTION)
