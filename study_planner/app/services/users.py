from datetime import datetime

from app.auth.passwords import hash_password, verify_password
from app.database.connection import db_session
from app.utils.errors import ConflictError, NotFoundError, UnauthorizedError, ValidationError


def _normalize_username(username: str) -> str:
    return username.strip()


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _validate_email(email: str) -> None:
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValidationError("Email format is invalid.")


def create_user(username: str, email: str, password: str) -> dict:
    username = _normalize_username(username)
    email = _normalize_email(email)

    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long.")

    _validate_email(email)
    password_hash = hash_password(password)
    created_at = datetime.utcnow().isoformat()

    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?",
            (username, email),
        )
        if cursor.fetchone():
            raise ConflictError("Username or email already exists.")

        cursor.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, created_at),
        )
        user_id = cursor.lastrowid

    return get_user_by_id(user_id)


def authenticate_user(username_or_email: str, password: str) -> dict:
    lookup = username_or_email.strip()
    lookup_email = lookup.lower()
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, password_hash, created_at FROM users WHERE username = ? OR email = ?",
            (lookup, lookup_email),
        )
        row = cursor.fetchone()

    if not row or not verify_password(password, row["password_hash"]):
        raise UnauthorizedError("Invalid credentials.")

    return {
        "id": row["id"],
        "username": row["username"],
        "email": row["email"],
        "created_at": row["created_at"],
    }


def get_user_by_id(user_id: int) -> dict:
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, created_at FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()

    if not row:
        raise NotFoundError("User not found.")

    return {
        "id": row["id"],
        "username": row["username"],
        "email": row["email"],
        "created_at": row["created_at"],
    }
