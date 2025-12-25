from database import get_connection
from schemas.case import CaseCreate , CaseResponse , CaseUpdate


def get_cases_by_owner(owner_username: str) -> list[CaseResponse]:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM cases WHERE owner_username = ?"
    cursor.execute(query , (owner_username,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row)for row in rows]

def create_case(case:CaseCreate , owner_username:str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO cases (title, description, owner_username)
    VALUES (?,?,?) 
    """
    cursor.execute(query, (case.title, case.description, owner_username))
    conn.commit()
    conn.close()


def delete_case(case_id: int , owner_username: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    DELETE FROM cases WHERE id = ? AND owner_username = ?
    """
    cursor.execute(query , (case_id , owner_username))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    return deleted > 0

def update_case(case_id: int, data: CaseUpdate , owner_username) -> bool:
    if not data:
        return False

    fields = []
    values = []

    for key, value in data.items():
        fields.append(f"{key} = ?")
        values.append(value)

    values.append(case_id)
    values.append(owner_username)

    query = f"""
    UPDATE cases
    SET {", ".join(fields)}
    WHERE id = ? AND owner_username = ?
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, tuple(values))
    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated > 0


