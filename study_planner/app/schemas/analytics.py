from datetime import date
from typing import Dict, List

from pydantic import BaseModel


class WeeklyTotal(BaseModel):
    week_start: date
    hours: float


class AnalyticsResponse(BaseModel):
    total_hours: float
    hours_per_subject: Dict[str, float]
    weekly_totals: List[WeeklyTotal]
    trend: str
