from uuid import uuid4

from tasks.calendars_statistics.models.client.events import DateTimeField, Event

SINGE_HOUR_EVENT = [
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(dateTime="2025-01-01T00:00:00+00:00", timeZone="Etc/UTC"),
        end=DateTimeField(dateTime="2025-01-01T01:00:00+00:00", timeZone="Etc/UTC"),
    )
]

TWO_HOUR_EVENTS = [
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(dateTime="2025-01-01T00:00:00+00:00", timeZone="Etc/UTC"),
        end=DateTimeField(dateTime="2025-01-01T01:00:00+00:00", timeZone="Etc/UTC"),
    ),
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(dateTime="2025-01-01T01:00:00+00:00", timeZone="Etc/UTC"),
        end=DateTimeField(dateTime="2025-01-01T02:00:00+00:00", timeZone="Etc/UTC"),
    ),
]

TWO_HOUR_EVENTS__SAME_HOUR = [
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(dateTime="2025-01-01T00:00:00+00:00", timeZone="Etc/UTC"),
        end=DateTimeField(dateTime="2025-01-01T01:00:00+00:00", timeZone="Etc/UTC"),
    ),
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(dateTime="2025-01-01T00:00:00+00:00", timeZone="Etc/UTC"),
        end=DateTimeField(dateTime="2025-01-01T01:00:00+00:00", timeZone="Etc/UTC"),
    ),
]

SINGLE_ALL_DAY_EVENT = [
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(date="2025-01-01"),
        end=DateTimeField(date="2025-01-02"),
    ),
]

TWO_ALL_DAY_EVENTS = [
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(date="2025-01-01"),
        end=DateTimeField(date="2025-01-02"),
    ),
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(date="2025-01-02"),
        end=DateTimeField(date="2025-01-03"),
    ),
]

TWO_ALL_DAY_EVENTS__SAME_DAY = [
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(date="2025-01-01"),
        end=DateTimeField(date="2025-01-02"),
    ),
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(date="2025-01-01"),
        end=DateTimeField(date="2025-01-02"),
    ),
]

SINGE_HOUR_EVENT__ENDS_NEXT_DAY = [
    Event(
        id=str(uuid4()),
        summary="test summary",
        start=DateTimeField(dateTime="2025-01-01T23:30:00+00:00", timeZone="Etc/UTC"),
        end=DateTimeField(dateTime="2025-01-02T00:30:00+00:00", timeZone="Etc/UTC"),
    ),
]
