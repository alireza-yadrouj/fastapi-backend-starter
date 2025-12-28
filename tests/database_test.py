import sqlite3

TEST_DB_NAME = "test_database.db"

def get_test_connection():
    conn = sqlite3.connect(TEST_DB_NAME)
    conn.row_factory=sqlite3.Row
    return conn

#creates tables ( users  and  cases)
def init_test_db():
    conn = get_test_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        owner_username TEXT
    )
    """)

    conn.commit()
    conn.close()
