from fastapi import APIRouter

from app.auth.jwt import create_token
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserPublic
from app.services import users as user_service
from app.utils.config import Settings

settings = Settings()
router = APIRouter()


@router.post("/register", response_model=UserPublic)
def register(payload: UserCreate):
    return user_service.create_user(payload.username, payload.email, payload.password)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin):
    user = user_service.authenticate_user(payload.username_or_email, payload.password)
    token = create_token(user["username"], user["id"], settings.jwt_secret, settings.jwt_expires_minutes)
    return TokenResponse(access_token=token, expires_in=settings.jwt_expires_minutes * 60)
