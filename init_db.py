import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'blog.db')

print("Creating DB at:", DB_PATH)

os.makedirs(BASE_DIR, exist_ok=True)  # Ensure directory exists

try:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        ''')
    print("✅ blog.db created successfully")
except Exception as e:
    print("❌ DB creation failed:", e)
