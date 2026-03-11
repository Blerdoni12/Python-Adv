import base64
import hashlib
import hmac
import os

from app.utils.errors import ValidationError


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def hash_password(password: str) -> str:
    if not password or len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return f"{_b64encode(salt)}${_b64encode(derived)}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_b64, hash_b64 = stored_hash.split("$", 1)
    except ValueError:
        return False

    salt = _b64decode(salt_b64)
    expected = _b64decode(hash_b64)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return hmac.compare_digest(derived, expected)
