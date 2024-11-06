import pytest

from aiogram.types.user import User

from src.calendars.services.calendars import CalendarService
from src.calendars.models.calendars import Calendar
from src.calendars.errors import CalendarDuplicateError, InvalidCalendarIDError
from src.calendars.constants.calendar_category import CalendarCategory


class TestCalendarService:
    async def test_add_calendar__new(
        self,
        calendar_service: CalendarService,
        user: User,
        calendar: Calendar,
    ):
        calendar_service._client._db[calendar.google_id] = calendar
        id_ = await calendar_service.add_calendar(
            user_tg_id=user.id,
            calendar_id=calendar.google_id,
        )

        assert id_ in calendar_service._calendar._db

    async def test_add_calendar__duplicate(
        self,
        calendar_service: CalendarService,
        user: User,
        calendar: Calendar,
    ):
        calendar_service._client._db[calendar.google_id] = calendar

        await calendar_service.add_calendar(user.id, calendar.google_id)

        with pytest.raises(CalendarDuplicateError):
            await calendar_service.add_calendar(user.id, calendar.google_id)

    async def test_add_calendar__invalid_id(
        self,
        calendar_service: CalendarService,
        user: User,
        calendar: Calendar,
    ):
        with pytest.raises(InvalidCalendarIDError):
            await calendar_service.add_calendar(user.id, calendar.google_id)

    async def test_update_calendar_category(
        self,
        calendar_service: CalendarService,
        user: User,
        calendar: Calendar,
    ):
        calendar_service._client._db[calendar.google_id] = calendar
        category = CalendarCategory.WORK

        calendar_id = await calendar_service.add_calendar(user.id, calendar.google_id)
        await calendar_service.update_calendar_category(
            calendar_id=calendar_id,
            calendar_category=category,
        )

        assert calendar_service._calendar._db[calendar_id].category == category
