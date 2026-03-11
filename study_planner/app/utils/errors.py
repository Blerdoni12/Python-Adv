from __future__ import annotations

from typing import Optional


class AppError(Exception):
    status_code = 400

    def __init__(self, message: str, *, status_code: Optional[int] = None, details: Optional[dict] = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code or self.status_code
        self.details = details or {}


class ValidationError(AppError):
    status_code = 422


class UnauthorizedError(AppError):
    status_code = 401


class ForbiddenError(AppError):
    status_code = 403


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409


class DatabaseError(AppError):
    status_code = 500
