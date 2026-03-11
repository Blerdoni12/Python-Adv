from fastapi import APIRouter, Depends

from app.auth.deps import get_current_user
from app.schemas.session import SessionCreate, SessionPublic
from app.services import sessions as session_service

router = APIRouter()


@router.get("/", response_model=list[SessionPublic])
def list_sessions(current_user: dict = Depends(get_current_user)):
    return session_service.get_sessions_for_user(current_user["id"])


@router.post("/", response_model=SessionPublic)
def create_session(payload: SessionCreate, current_user: dict = Depends(get_current_user)):
    return session_service.create_session(
        current_user["id"],
        payload.subject,
        payload.duration,
        payload.notes,
        payload.session_date,
    )
