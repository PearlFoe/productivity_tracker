import datetime

from pydantic import BaseModel


class Schedule(BaseModel):
    user_id: str
    name: str
    time: datetime.time


class DefaultWeeklyReportSchedule(Schedule):
    name: str = "Report for the last week"
    time: datetime.time = datetime.time(hour=10, tzinfo=datetime.UTC)
