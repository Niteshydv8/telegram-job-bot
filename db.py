import sqlite3
from datetime import datetime

# Create/connect to the DB
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    join_date TEXT,
    premium INTEGER DEFAULT 0,
    messages_used INTEGER DEFAULT 0,
    daily_checkin TEXT,
    total_invites INTEGER DEFAULT 0,
    total_messages INTEGER DEFAULT 0
)
""")

# Create giveaways table
cursor.execute("""
CREATE TABLE IF NOT EXISTS giveaways (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    max_winners INTEGER DEFAULT 1,
    status TEXT DEFAULT 'active',
    min_messages INTEGER DEFAULT 0,
    min_days_in_group INTEGER DEFAULT 0,
    require_checkin INTEGER DEFAULT 0,
    created_by INTEGER
)
""")

# Create giveaway entries table
cursor.execute("""
CREATE TABLE IF NOT EXISTS giveaway_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    giveaway_id INTEGER,
    user_id INTEGER,
    entry_date TEXT,
    bonus_entries INTEGER DEFAULT 0,
    tasks_completed TEXT,
    FOREIGN KEY (giveaway_id) REFERENCES giveaways(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(giveaway_id, user_id)
)
""")

# Create tasks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task_type TEXT,
    task_date TEXT,
    points INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# Create winners table
cursor.execute("""
CREATE TABLE IF NOT EXISTS giveaway_winners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    giveaway_id INTEGER,
    user_id INTEGER,
    won_date TEXT,
    notified INTEGER DEFAULT 0,
    FOREIGN KEY (giveaway_id) REFERENCES giveaways(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
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
