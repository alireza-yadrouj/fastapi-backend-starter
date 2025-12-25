from database import get_connection
from core.security import hash_password


def create_user(username: str, password: str , role:str="user"):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?,?)",
        (username, hashed_password,role)
)


    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return {"id": user_id, "username": username , "role": role}
    


def get_user_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password, role FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    return user
