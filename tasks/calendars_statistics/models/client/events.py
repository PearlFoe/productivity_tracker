import datetime as dt
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator

from tasks.calendars_statistics.constants import (
    GOOGLE_API_DATE_RESPONSE_FORMAT,
    GOOGLE_API_DATETIME_RESPONSE_FORMAT,
)


class DateTimeField(BaseModel):
    date: dt.date | None = None
    datetime: dt.datetime | None = Field(None, alias="dateTime")
    timezone: str = Field(None, alias="timeZone")

    @field_validator("datetime", mode="before")
    @classmethod
    def validate_datetime(cls: "DateTimeField", v: str) -> dt.datetime:
        dt_ = "".join(v.rsplit(":", maxsplit=1))
        return dt.datetime.strptime(dt_, GOOGLE_API_DATETIME_RESPONSE_FORMAT)  # noqa: DTZ007

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls: "DateTimeField", v: str) -> dt.date:
        dt_ = "".join(v.rsplit(":", maxsplit=1))
        return dt.datetime.strptime(dt_, GOOGLE_API_DATE_RESPONSE_FORMAT).date()  # noqa: DTZ007


class MeetingResponseStatus(StrEnum):
    NEEDS_ACTION = "needsAction"
    DECLINE = "declined"
    TENTATIVE = "tentative"
    ACCEPTED = "accepted"


class Attendee(BaseModel):
    self: bool
    status: MeetingResponseStatus = Field(alias="responseStatus")


class Event(BaseModel):
    id: str
    summary: str | None = None
    attendees: list[Attendee] | None = None
    start: DateTimeField
    end: DateTimeField
