"""Seed the roles table with default roles.

Usage: python migrate_add_default_roles.py path/to/app.db
"""
import sqlite3
import sys

DEFAULT_ROLES = ["admin", "editor", "viewer"]


def migrate(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS roles ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL)"
    )
    for role in DEFAULT_ROLES:
        cur.execute("INSERT INTO roles (name) VALUES (?)", (role,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    migrate(sys.argv[1])
    print("roles migration complete")
