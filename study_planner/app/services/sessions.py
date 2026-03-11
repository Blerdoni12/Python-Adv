from datetime import date

from app.database.connection import db_session
from app.utils.errors import NotFoundError, ValidationError


def _validate_subject(subject: str) -> str:
    subject = subject.strip()
    if len(subject) < 2:
        raise ValidationError("Subject must be at least 2 characters long.")
    return subject


def create_session(user_id: int, subject: str, duration: int, notes: str | None, session_date: date) -> dict:
    subject = _validate_subject(subject)
    if duration <= 0:
        raise ValidationError("Duration must be greater than 0.")

    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO study_sessions (user_id, subject, duration, notes, session_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, subject, int(duration), notes, session_date.isoformat()),
        )
        session_id = cursor.lastrowid

    return get_session_by_id(user_id, session_id)


def get_sessions_for_user(user_id: int) -> list[dict]:
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, user_id, subject, duration, notes, session_date FROM study_sessions WHERE user_id = ? ORDER BY session_date DESC",
            (user_id,),
        )
        rows = cursor.fetchall()

    return [
        {
            "id": row["id"],
            "user_id": row["user_id"],
            "subject": row["subject"],
            "duration": row["duration"],
            "notes": row["notes"],
            "session_date": row["session_date"],
        }
        for row in rows
    ]


def get_session_by_id(user_id: int, session_id: int) -> dict:
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, user_id, subject, duration, notes, session_date FROM study_sessions WHERE id = ? AND user_id = ?",
            (session_id, user_id),
        )
        row = cursor.fetchone()

    if not row:
        raise NotFoundError("Session not found.")

    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "subject": row["subject"],
        "duration": row["duration"],
        "notes": row["notes"],
        "session_date": row["session_date"],
    }
