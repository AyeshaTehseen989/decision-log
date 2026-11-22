from typing import Literal

from pydantic import BaseModel, Field

Status = Literal["proposed", "accepted", "superseded"]

class DecisionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    context: str =Field(min_length=1)
    decision: str = Field(min_length=1)
    status: Status = "proposed"

class Decision(DecisionCreate):
    id: int
    created_at: str

