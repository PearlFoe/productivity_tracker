from uuid import UUID

from pydantic import BaseModel


class Calendar(BaseModel):
    name: str
    id: UUID | None = None
    description: str | None = None
    category: str | None = None
    timezone: str | None = None
