from uuid import UUID

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import Provide, inject

from pt_bot.core.models.user import User
from pt_bot.core.utils import inject_user

from .constants.messages import CalendarMessages
from .containers import CalendarContainer
from .errors import CalendarDuplicateError, InvalidCalendarIDError
from .fsm import CalendarState
from .keyboards import CalendarKeyboard
from .services.calendars import CalendarService

router = Router()


@router.message(Command("calendar"))
async def calendar_command(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=CalendarMessages.REQUEST_LINK)
    await state.set_state(CalendarState.LINK)


@router.message(CalendarState.LINK)
@inject
@inject_user
async def calendar_link_processing(
    message: types.Message,
    state: FSMContext,
    user: User,
    calendar_service: CalendarService = Provide[CalendarContainer.calendar_service],
) -> None:
    try:
        calendar_id = await calendar_service.add_calendar(user, message.text)
    except InvalidCalendarIDError:
        await message.answer(text=CalendarMessages.INVALID_CALENDAR_LINK)
        await state.clear()
        return
    except CalendarDuplicateError:
        await message.answer(text=CalendarMessages.CALENDAR_DUPLICATE)
        await state.clear()
        return

    await message.answer(text=CalendarMessages.CHOOSE_CATEGORY, reply_markup=CalendarKeyboard.category_kb())
    await state.set_state(CalendarState.CATEGORY)
    await state.set_data(str(calendar_id))


@router.callback_query(CalendarState.CATEGORY)
@inject
async def calendar_category_choice(
    callback: types.CallbackQuery,
    state: FSMContext,
    calendar_service: CalendarService = Provide[CalendarContainer.calendar_service],
) -> None:
    await calendar_service.update_calendar_category(
        calendar_id=UUID(await state.get_data()),
        calendar_category=callback.data,
    )
    await callback.message.edit_text(text=CalendarMessages.CALENDAR_ADDED_SUCCESSFULLY)
    await state.clear()
