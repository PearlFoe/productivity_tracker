from uuid import UUID

from pydantic import BaseModel


class Report(BaseModel):
    user_id: UUID
    schedule_id: UUID | None
    data: str
    name: str = "report"
    file_name: str = "report.html"
