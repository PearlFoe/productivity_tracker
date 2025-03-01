from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class StatisticsFilters(BaseModel):
    user_id: UUID
    calendar_id: UUID
    calendar_google_id: str
    start: datetime
    end: datetime
