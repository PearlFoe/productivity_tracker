from pydantic import BaseModel, Field

class Calendar(BaseModel):
    id: str
    summary: str
    time_zome: str = Field(alias="timeZone")
