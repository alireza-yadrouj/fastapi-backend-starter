from database import get_connection

def get_all_cases():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases")
    rows = cursor.fetchall()
    conn.close()
    return rows
