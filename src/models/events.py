import datetime

from pydantic import BaseModel


class Event(BaseModel):
    id: str
    created: str
    start: datetime.datetime
    end: datetime.datetime