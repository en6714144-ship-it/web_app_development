import sqlite3
import os

# DB_PATH will point to root_directory/instance/database.db
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # Using Row to easily convert output to dicts
    conn.row_factory = sqlite3.Row
    # Ensure foreign key constraints are enforced
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
