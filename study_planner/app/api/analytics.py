from fastapi import APIRouter, Depends

from app.auth.deps import get_current_user
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics import compute_analytics

router = APIRouter()


@router.get("/", response_model=AnalyticsResponse)
def get_analytics(current_user: dict = Depends(get_current_user)):
    return compute_analytics(current_user["id"])
