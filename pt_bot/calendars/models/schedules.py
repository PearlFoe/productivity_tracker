import datetime
from uuid import UUID

from pydantic import BaseModel


class Schedule(BaseModel):
    user_id: UUID
    name: str
    time: datetime.time


class DefaultWeeklyReportSchedule(Schedule):
    name: str = "Report for the last week"
    time: datetime.time = datetime.time(hour=10, tzinfo=datetime.UTC)
