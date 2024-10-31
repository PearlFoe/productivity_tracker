from pydantic import BaseModel, Field


class Calendar(BaseModel):
    id: str
    summary: str
    description: str
    timezone: str = Field(alias="timeZone")
    primary: bool
