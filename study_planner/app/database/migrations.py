from app.database.connection import get_db_connection


def init_db() -> None:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS study_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            deadline TEXT NOT NULL,
            priority TEXT NOT NULL,
            estimated_hours REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            duration INTEGER NOT NULL,
            notes TEXT,
            session_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_plans_user_id ON study_plans(user_id);
        CREATE INDEX IF NOT EXISTS idx_plans_deadline ON study_plans(deadline);
        CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON study_sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_date ON study_sessions(session_date);
        """
    )

    conn.commit()
    conn.close()
