from datetime import date
from uuid import UUID

from pydantic import BaseModel


class ReportFiler(BaseModel):
    user_id: UUID
    start: date
    end: date
