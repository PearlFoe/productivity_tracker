from datetime import datetime

from pydantic import BaseModel, field_validator

from tasks.calendars_statistics.constants import GOOGLE_API_DATETIME_RESPONSE_FORMAT



class Event(BaseModel):
    id: str
    summary: str
    start: datetime
    end: datetime

    @field_validator("start", "end", mode="before")
    @classmethod
    def validate_date(cls: "Event", v: dict[str, str]) -> datetime:
        dt = "".join(v["dateTime"].rsplit(":", maxsplit=1))
        return datetime.strptime(dt, GOOGLE_API_DATETIME_RESPONSE_FORMAT)  # noqa: DTZ007
