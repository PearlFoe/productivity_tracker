from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from .fsm import CalendarState
from .constants.messages import CalendarMessages
from .keyboards import CalendarKeyboard

router = Router()


@router.message(Command("/calendar"))
async def calendar_command(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=CalendarMessages.REQUEST_LINK)
    await state.set_state(CalendarState.LINK)


@router.message(CalendarState.LINK)
async def calendar_link_processing(message: types.Message, state: FSMContext) -> None:
    # TODO: validate url
    await message.answer(text=CalendarMessages.CHOOSE_CATEGORY, reply_markup=CalendarKeyboard.category_kb)
    await state.set_state(CalendarState.CATEGORY)  # pass somehow calendar id with the state


@router.callback_query(CalendarState.CATEGORY)
async def calendar_category_choice(callback: types.CallbackQuery, state: FSMContext) -> None:
    # save category choice
    await callback.message.edit_text(text=CalendarMessages.CALENDAR_ADDED_SUCCESSFULLY)
    await state.clear()
