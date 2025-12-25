from database import get_connection

def reset_cases_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    # حذف جدول قبلی اگر وجود دارد
    cursor.execute("DROP TABLE IF EXISTS cases")
    
    # ساخت جدول جدید با ستون owner_username
    cursor.execute("""
        CREATE TABLE cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            owner_username TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
