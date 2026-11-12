"""
Initialise EduPath SG SQLite database.
Run: python scripts/init_db.py
"""
import sys, bcrypt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from utils.config import DB_PATH
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('parent','student','teacher')),
    full_name TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    question TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    chunks_json TEXT DEFAULT '[]',
    created_at TEXT
);
"""

DEMO_USERS = [
    ("parent@edupathsg.sg",  "Parent123!",  "parent",  "Demo Parent"),
    ("student@edupathsg.sg", "Student123!", "student", "Demo Student"),
    ("teacher@edupathsg.sg", "Teacher123!", "teacher", "Demo Teacher"),
]


def init():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)

    for email, pw, role, name in DEMO_USERS:
        existing = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if not existing:
            pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
            conn.execute(
                "INSERT INTO users (email, password_hash, role, full_name) VALUES (?,?,?,?)",
                (email, pw_hash, role, name)
            )
            print(f"  Created: {email} ({role})")
        else:
            print(f"  Exists:  {email}")

    conn.commit()
    conn.close()
    print(f"\nDatabase ready at: {DB_PATH}")


if __name__ == "__main__":
    print("Initialising EduPath SG database...")
    init()
