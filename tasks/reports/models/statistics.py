from datetime import date

from pydantic import BaseModel


class DailyStatistics(BaseModel):
    calendat_name: str
    date: date
    minutes: int = 0
