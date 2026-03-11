from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    subject: str = Field(..., min_length=2, max_length=100)
    duration: int = Field(..., gt=0)
    notes: Optional[str] = Field(default=None, max_length=500)
    session_date: date


class SessionPublic(BaseModel):
    id: int
    user_id: int
    subject: str
    duration: int
    notes: Optional[str]
    session_date: date
