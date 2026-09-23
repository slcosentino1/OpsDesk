from pydantic import BaseModel, Field


class Ticket(BaseModel):
    id: str = Field(min_length=1)
    title: str
    status: str
    requester: str
    summary: str
