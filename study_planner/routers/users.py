import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from database import get_db_connection
from auth.security import get_api_key

router = APIRouter()


# ---------------- Pydantic Models ----------------

class User(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


# ---------------- GET ALL USERS ----------------

@router.get("/", response_model=List[User])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()

    conn.close()

    return [
        {"id": user[0], "name": user[1], "email": user[2]}
        for user in users
    ]


# ---------------- CREATE USER ----------------

@router.post("/", response_model=User)
def create_user(
    user: UserCreate,
    api_key: str = Depends(get_api_key),
):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, user.email),
        )
        conn.commit()

        user_id = cursor.lastrowid
        return User(id=user_id, name=user.name, email=user.email)

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user.email}' already exists.",
        )

    finally:
        conn.close()


# ---------------- UPDATE USER ----------------

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserCreate,
    _: str = Depends(get_api_key),
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (user.name, user.email, user_id),
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    conn.commit()
    conn.close()

    return User(id=user_id, name=user.name, email=user.email)


# ---------------- DELETE USER ----------------

@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    _: str = Depends(get_api_key),
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    conn.commit()
    conn.close()

    return {"detail": "User deleted successfully"}