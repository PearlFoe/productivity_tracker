from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    telegram_id: int
