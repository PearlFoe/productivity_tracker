from uuid import UUID

from pydantic import BaseModel


class Calendar(BaseModel):
    id: UUID
    user_id: UUID
    google_id: str
    name: str
    timezone: str
    description: str | None = None
    category: str | None = None
