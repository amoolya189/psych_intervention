import sqlite3

# Use your correct DB name
DB_PATH = "database.db"  

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # --- Forum Posts Table ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forum_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        content TEXT,
        categories TEXT,
        file_path TEXT,
        likes INTEGER DEFAULT 0,
        timestamp TEXT,
        parent_id INTEGER
    )
    """)

    # --- Bookings Table ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        counsellor TEXT
    )
    """)

    # ✅ Ensure all required columns exist in bookings
    cursor.execute("PRAGMA table_info(bookings)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    # Now we want: student_name, time, email
    required_columns = ["student_name", "time", "email"]

    for col in required_columns:
        if col not in existing_columns:
            cursor.execute(f"ALTER TABLE bookings ADD COLUMN {col} TEXT")

    conn.commit()
    conn.close()
