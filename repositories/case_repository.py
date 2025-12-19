from database import get_connection
from schemas.case import CaseCreate


def get_all_cases():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row)for row in rows]

def create_case(case:CaseCreate):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO cases (title, description)
    VALUES (?,?) 
    """
    cursor.execute(query, (case.title, case.description))
    conn.commit()
    conn.close()

