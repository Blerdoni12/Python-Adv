from typing import List

from pydantic import BaseModel


class ResourceItem(BaseModel):
    title: str
    url: str
    source: str


class ResourceResponse(BaseModel):
    results: List[ResourceItem]
