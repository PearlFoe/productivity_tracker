from datetime import date

from pydantic import BaseModel


class DailyStatistics(BaseModel):
    calendar_name: str
    date: date
    minutes: int = 0


class StatisticsExtremum(BaseModel):
    all_calendars_minutes_sum: int
    one_calendar_minutes_sum: int
