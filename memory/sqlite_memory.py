import sqlite3
from pathlib import Path


DB_PATH = "data/jarvis_memory.db"


def get_connection() -> sqlite3.Connection:
    Path("data").mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_memory() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_memory(category: str, content: str) -> str:
    with get_connection() as connection:
        existing = connection.execute(
            """
            SELECT id
            FROM memories
            WHERE category = ? AND content = ?
            """,
            (category, content),
        ).fetchone()

        if existing:
            return "Memory already exists."

        connection.execute(
            """
            INSERT INTO memories (category, content)
            VALUES (?, ?)
            """,
            (category, content),
        )

    return "Memory saved."


def get_memories(limit: int = 10) -> list[tuple]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, category, content, created_at
            FROM memories
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()


def search_memories(keyword: str) -> list[tuple]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, category, content, created_at
            FROM memories
            WHERE content LIKE ?
            ORDER BY id DESC
            """,
            (f"%{keyword}%",),
        )

        return cursor.fetchall()

def delete_memory(memory_id: int) -> str:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (memory_id,),
        )

        if cursor.rowcount == 0:
            return "Memory not found."

    return "Memory deleted."