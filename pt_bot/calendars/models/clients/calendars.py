from pydantic import BaseModel, Field


class Calendar(BaseModel):
    id: str
    summary: str
    timezone: str = Field(alias="timeZone")
    description: str | None = Field(None)
