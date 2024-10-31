from uuid import UUID

from pydantic import BaseModel


class Calendar(BaseModel):
    google_id: str
    name: str
    timezone: str
    primary: bool
    id: UUID | None = None
    description: str | None = None
    category: str | None = None
