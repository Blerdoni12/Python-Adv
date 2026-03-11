from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.jwt import verify_token
from app.utils.config import Settings
from app.utils.errors import UnauthorizedError

settings = Settings()
security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None or not credentials.credentials:
        raise UnauthorizedError("Missing authorization token.")

    payload = verify_token(credentials.credentials, settings.jwt_secret)
    user_id = payload.get("uid")

    if not isinstance(user_id, int):
        raise UnauthorizedError("Invalid token payload.")

    from app.services.users import get_user_by_id

    return get_user_by_id(user_id)
