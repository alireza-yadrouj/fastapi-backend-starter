from database import get_connection
from schemas.case import CaseCreate , CaseResponse , CaseUpdate


def get_all_cases() -> list[CaseResponse]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row)for row in rows]

def create_case(case:CaseCreate) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO cases (title, description)
    VALUES (?,?) 
    """
    cursor.execute(query, (case.title, case.description))
    conn.commit()
    conn.close()


def delete_case(case_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    DELETE FROM cases WHERE id = ?
    """
    cursor.execute(query , (case_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    return deleted > 0

def update_case(case_id: int, data: CaseUpdate) -> bool:
    if not data:
        return False

    fields = []
    values = []

    for key, value in data.items():
        fields.append(f"{key} = ?")
        values.append(value)

    values.append(case_id)

    query = f"""
    UPDATE cases
    SET {", ".join(fields)}
    WHERE id = ?
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, tuple(values))
    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated > 0


