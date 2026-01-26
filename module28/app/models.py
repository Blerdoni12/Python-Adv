from pydantic import BaseModel
from typing import Optional

class item(BaseModel):
    id:Optional[int]= None
    name:str
    description: Optional[str]= None

