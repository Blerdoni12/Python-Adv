from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class PriorityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class PlanStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class PlanCreate(BaseModel):
    subject: str = Field(..., min_length=2, max_length=100)
    deadline: date
    priority: PriorityLevel = PriorityLevel.medium
    estimated_hours: float = Field(..., gt=0)
    status: PlanStatus = PlanStatus.pending


class PlanUpdate(BaseModel):
    subject: str = Field(..., min_length=2, max_length=100)
    deadline: date
    priority: PriorityLevel
    estimated_hours: float = Field(..., gt=0)
    status: PlanStatus


class PlanPublic(BaseModel):
    id: int
    user_id: int
    subject: str
    deadline: date
    priority: PriorityLevel
    estimated_hours: float
    status: PlanStatus
