from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudyPlanBase(BaseModel):
    title:str
    subject:str
    study_date:datetime
    duration_minutes:int
    notes: Optional[str]= None
    completed:bool = False

class StudyPlanCreate(StudyPlanBase):
    pass

class StudyPlanResponse(StudyPlanBase):
    id:int
    user_id:int

class StudyPlan(StudyPlanBase):
    id:int
    user_id:int