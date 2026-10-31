
import sqlite3
from pathlib import Path
from datetime import datetime


DATABASE_PATH = (
    Path(__file__).resolve().parents[2] / "aura.db"
)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
            )
        """)


def create_conversation(title="New Chat"):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO conversations (title, created_at)
            VALUES (?, ?)
            """,
            (title, datetime.now().isoformat())
        )

        return cursor.lastrowid


def save_message(conversation_id, role, content):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO messages (
                conversation_id, role, content, created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                conversation_id,
                role,
                content,
                datetime.now().isoformat()
            )
        )


def get_conversations():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM conversations
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


def get_messages(conversation_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,)
        ).fetchall()

        return [dict(row) for row in rows]


def update_conversation_title(conversation_id, title):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE conversations
            SET title = ?
            WHERE id = ?
            """,
            (title, conversation_id)
        )
