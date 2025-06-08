import sqlite3

# Create/connect to the DB
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    join_date TEXT,
    premium INTEGER DEFAULT 0,
    messages_used INTEGER DEFAULT 0
)
""")
conn.commit()

# Add or update user
def add_user(user_id, username, full_name, join_date):
    cursor.execute("""
    INSERT OR IGNORE INTO users (id, username, full_name, join_date) 
    VALUES (?, ?, ?, ?)
    """, (user_id, username, full_name, join_date))
    conn.commit()

# Get user info
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return cursor.fetchone()

# Mark user as premium
def set_premium(user_id, value=1):
    cursor.execute("UPDATE users SET premium=? WHERE id=?", (value, user_id))
    conn.commit()

# Count messages
def increment_message(user_id):
    cursor.execute("UPDATE users SET messages_used = messages_used + 1 WHERE id=?", (user_id,))
    conn.commit()
