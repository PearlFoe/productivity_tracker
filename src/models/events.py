import datetime

from pydantic import BaseModel, field_validator

from constants import DT_RESPONSE_FORMAT

class Event(BaseModel):
    id: str
    created: str
    start: datetime.datetime
    end: datetime.datetime

    @field_validator("start", "end", mode="before")
    @classmethod
    def date_validator(cls, v: dict[str, str]) -> datetime.datetime:
        dt = "".join(v["dateTime"].rsplit(":", maxsplit=1))
        return datetime.datetime.strptime(dt, DT_RESPONSE_FORMAT)