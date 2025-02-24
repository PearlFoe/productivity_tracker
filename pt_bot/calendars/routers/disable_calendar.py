from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import Provide, inject

from pt_bot.core.buttons.base import Button
from pt_bot.core.models.user import User
from pt_bot.core.utils import inject_user

from ..constants.buttons import MenuButtons
from ..constants.messages import CalendarMessages
from ..containers import CalendarContainer
from ..fsm import CalendarState
from ..keyboards import CalendarKeyboard
from ..services.calendars import CalendarService

router = Router()


@router.callback_query(lambda c: c.data == MenuButtons.DISABLE_CALENDAR.callback_data)
@inject
@inject_user
async def choose_calendar_to_disable(
    callback: types.CallbackQuery,
    state: FSMContext,
    user: User,
    calendar_service: CalendarService = Provide[CalendarContainer.calendar_service],
) -> None:
    calendar_names = await calendar_service.get_calendar_names(user)

    buttons = [Button(text=name, callback_data=name) for name in calendar_names]

    await callback.message.edit_text(
        text=CalendarMessages.REQUEST_LINK,
        reply_markup=CalendarKeyboard.disable_calendar_kb(buttons),
    )
    await state.set_state(CalendarState.CHOOSE_NAME)


@router.callback_query(CalendarState.CHOOSE_NAME)
@inject
@inject_user
async def disable_calendar(
    callback: types.CallbackQuery,
    state: FSMContext,
    user: User,
    calendar_service: CalendarService = Provide[CalendarContainer.calendar_service],
) -> None:
    await calendar_service.disable_calendar(user=user, calendar_name=callback.data)
    await callback.message.edit_text(text=CalendarMessages.СALENDAR_DISABLED_SUCCESSFULLY)
    await state.clear()
