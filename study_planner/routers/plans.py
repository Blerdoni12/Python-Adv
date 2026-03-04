import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from database import get_db_connection
from auth.security import get_api_key

router = APIRouter()


# ---------------- Pydantic Models ----------------

class Plan(BaseModel):
    id: int
    subject: str
    study_date: str
    duration_minutes: int
    status: str
    user_id: int


class PlanCreate(BaseModel):
    subject: str
    study_date: str
    duration_minutes: int
    status: str = "pending"
    user_id: int


# ---------------- GET ALL PLANS ----------------

@router.get("/", response_model=List[Plan])
def get_plans():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, subject, study_date, duration_minutes, status, user_id
        FROM plans
    """)
    plans = cursor.fetchall()

    conn.close()

    return [
        {
            "id": plan[0],
            "subject": plan[1],
            "study_date": plan[2],
            "duration_minutes": plan[3],
            "status": plan[4],
            "user_id": plan[5],
        }
        for plan in plans
    ]


# ---------------- CREATE PLAN ----------------

@router.post("/", response_model=Plan)
def create_plan(plan: PlanCreate, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Optional: check if user exists
        cursor.execute("SELECT id FROM users WHERE id = ?", (plan.user_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="User not found")

        cursor.execute("""
            INSERT INTO plans (subject, study_date, duration_minutes, status, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            plan.subject,
            plan.study_date,
            plan.duration_minutes,
            plan.status,
            plan.user_id
        ))

        conn.commit()
        plan_id = cursor.lastrowid

        return Plan(id=plan_id, **plan.dict())

    finally:
        conn.close()


# ---------------- UPDATE PLAN ----------------

@router.put("/{plan_id}", response_model=Plan)
def update_plan(plan_id: int, plan: PlanCreate, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE plans
        SET subject = ?, study_date = ?, duration_minutes = ?, status = ?, user_id = ?
        WHERE id = ?
    """, (
        plan.subject,
        plan.study_date,
        plan.duration_minutes,
        plan.status,
        plan.user_id,
        plan_id
    ))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Plan not found")

    conn.commit()
    conn.close()

    return Plan(id=plan_id, **plan.dict())


# ---------------- DELETE PLAN ----------------

@router.delete("/{plan_id}", response_model=dict)
def delete_plan(plan_id: int, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM plans WHERE id = ?", (plan_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Plan not found")

    conn.commit()
    conn.close()

    return {"detail": "Plan deleted successfully"}