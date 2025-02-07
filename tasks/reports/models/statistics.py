from datetime import date

from pydantic import BaseModel


class DailyStatistics(BaseModel):
    calendar_name: str
    date: date
    minutes: int = 0
