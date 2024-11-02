import sqlite3

def create_connection():
    conn = sqlite3.connect('cases.db')
    return conn

def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            category TEXT,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

def add_report(user_id, category, details):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (user_id, category, details) VALUES (?, ?, ?)",
                   (user_id, category, details))
    conn.commit()
    conn.close()

def get_reports():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE status = 'Pending'")
    reports = cursor.fetchall()
    conn.close()
    return reports

# initialize_db()
