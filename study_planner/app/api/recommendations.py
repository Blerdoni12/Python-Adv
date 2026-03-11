from fastapi import APIRouter, Depends

from app.auth.deps import get_current_user
from app.services.recommendations import get_recommendations

router = APIRouter()


@router.get("/")
def recommendations(current_user: dict = Depends(get_current_user)):
    return {"recommendations": get_recommendations(current_user["id"])}
