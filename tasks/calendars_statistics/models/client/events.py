from datetime import datetime

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: str
    summary: str
    start: datetime
    end: datetime
    timezone: str = Field(alias="timeZone")
