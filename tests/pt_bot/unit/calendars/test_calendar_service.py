import pytest

from pt_bot.calendars.constants.calendar_category import CalendarCategory
from pt_bot.calendars.errors import CalendarDuplicateError, InvalidCalendarIDError
from pt_bot.calendars.models.calendars import Calendar
from pt_bot.calendars.services.calendars import CalendarService
from pt_bot.core.models.user import User


class TestCalendarService:
    async def test_add_calendar__new(
        self,
        calendar_service: CalendarService,
        user: User,
        calendar: Calendar,
    ):
        calendar_service._client._db[calendar.google_id] = calendar
        id_ = await calendar_service.add_calendar(
            user=user,
            calendar_id=calendar.google_id,
        )

        assert id_ in calendar_service._calendar._db["calendars"]
        assert calendar_service._calendar._db["schedules"]

    async def test_add_calendar__duplicate(
        self,
        calendar_service: CalendarService,
        user: User,
        calendar: Calendar,
    ):
        calendar_service._client._db[calendar.google_id] = calendar

        await calendar_service.add_calendar(user, calendar.google_id)

        with pytest.raises(CalendarDuplicateError):
            await calendar_service.add_calendar(user, calendar.google_id)

    async def test_add_calendar__invalid_id(
        self,
        calendar_service: CalendarService,
        user: User,
        calendar: Calendar,
    ):
        with pytest.raises(InvalidCalendarIDError):
            await calendar_service.add_calendar(user, calendar.google_id)

    async def test_update_calendar_category(
        self,
        calendar_service: CalendarService,
        user: User,
        calendar: Calendar,
    ):
        calendar_service._client._db[calendar.google_id] = calendar
        category = CalendarCategory.WORK

        calendar_id = await calendar_service.add_calendar(user, calendar.google_id)
        await calendar_service.update_calendar_category(
            calendar_id=calendar_id,
            calendar_category=category,
        )

        assert calendar_service._calendar._db["calendars"][calendar_id].category == category
