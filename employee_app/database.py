import sqlite3

DB_NAME = "expense_manager.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            reviewer INTEGER,
            comment TEXT,
            review_date TEXT,
            FOREIGN KEY (expense_id) REFERENCES expenses(id),
            FOREIGN KEY (reviewer) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('employee1', 'pass123', 'employee')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('manager1', 'admin123', 'manager')
    """)

    conn.commit()
    conn.close()