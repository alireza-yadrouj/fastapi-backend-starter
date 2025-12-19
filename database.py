import sqlite3

DB_name = "database.db"

def get_connection():
    conn = sqlite3.connect(DB_name)
    conn.row_factory = sqlite3.Row
    return conn

