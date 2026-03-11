from fastapi import APIRouter, Depends, Query

from app.auth.deps import get_current_user
from app.schemas.resource import ResourceResponse
from app.services.resources import search_resources

router = APIRouter()


@router.get("/", response_model=ResourceResponse)
def resources(topic: str = Query(..., min_length=2), _: dict = Depends(get_current_user)):
    results = search_resources(topic)
    return {"results": results}
