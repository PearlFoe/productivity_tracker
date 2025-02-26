from uuid import UUID

from pydantic import BaseModel


class StatisticsParsingConfig(BaseModel):
    user_id: UUID
    skip_all_day_events: bool
    skip_rejected_meetings: bool
