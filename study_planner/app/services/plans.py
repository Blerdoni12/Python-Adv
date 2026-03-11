from datetime import date

from app.database.connection import db_session
from app.utils.errors import NotFoundError, ValidationError


def _validate_subject(subject: str) -> str:
    subject = subject.strip()
    if len(subject) < 2:
        raise ValidationError("Subject must be at least 2 characters long.")
    return subject


def create_plan(user_id: int, subject: str, deadline: date, priority: str, estimated_hours: float, status: str) -> dict:
    subject = _validate_subject(subject)
    if estimated_hours <= 0:
        raise ValidationError("Estimated hours must be greater than 0.")

    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO study_plans (user_id, subject, deadline, priority, estimated_hours, status) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, subject, deadline.isoformat(), priority, float(estimated_hours), status),
        )
        plan_id = cursor.lastrowid

    return get_plan_by_id(user_id, plan_id)


def get_plans_for_user(user_id: int) -> list[dict]:
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, user_id, subject, deadline, priority, estimated_hours, status FROM study_plans WHERE user_id = ? ORDER BY deadline ASC",
            (user_id,),
        )
        rows = cursor.fetchall()

    return [
        {
            "id": row["id"],
            "user_id": row["user_id"],
            "subject": row["subject"],
            "deadline": row["deadline"],
            "priority": row["priority"],
            "estimated_hours": row["estimated_hours"],
            "status": row["status"],
        }
        for row in rows
    ]


def get_plan_by_id(user_id: int, plan_id: int) -> dict:
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, user_id, subject, deadline, priority, estimated_hours, status FROM study_plans WHERE id = ? AND user_id = ?",
            (plan_id, user_id),
        )
        row = cursor.fetchone()

    if not row:
        raise NotFoundError("Plan not found.")

    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "subject": row["subject"],
        "deadline": row["deadline"],
        "priority": row["priority"],
        "estimated_hours": row["estimated_hours"],
        "status": row["status"],
    }


def update_plan(user_id: int, plan_id: int, subject: str, deadline: date, priority: str, estimated_hours: float, status: str) -> dict:
    subject = _validate_subject(subject)
    if estimated_hours <= 0:
        raise ValidationError("Estimated hours must be greater than 0.")

    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE study_plans SET subject = ?, deadline = ?, priority = ?, estimated_hours = ?, status = ? WHERE id = ? AND user_id = ?",
            (subject, deadline.isoformat(), priority, float(estimated_hours), status, plan_id, user_id),
        )
        if cursor.rowcount == 0:
            raise NotFoundError("Plan not found.")

    return get_plan_by_id(user_id, plan_id)


def delete_plan(user_id: int, plan_id: int) -> None:
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM study_plans WHERE id = ? AND user_id = ?",
            (plan_id, user_id),
        )
        if cursor.rowcount == 0:
            raise NotFoundError("Plan not found.")
