from flask import Flask
from threading import Thread
import os
import logging
import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)

# -----------------------------
# Flask Web Server for Render
# -----------------------------
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "🤖 Bot is running!"

def run():
    web_app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# -----------------------------
# Environment Variables
# -----------------------------
BOT_TOKEN = os.environ['TELEGRAM_TOKEN']
ADMIN_ID = 5762701937  # Replace with your actual Telegram user ID

# -----------------------------
# SQLite Database Functions
# -----------------------------
db_path = "users.db"

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    is_premium INTEGER DEFAULT 0,
                    messages_used INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def is_premium(user_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT is_premium FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == 1

def increment_messages(user_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE users SET messages_used = messages_used + 1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def get_messages_used(user_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT messages_used FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def total_users():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count

def premium_users():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE is_premium=1")
    count = c.fetchone()[0]
    conn.close()
    return count

# -----------------------------
# Telegram Bot Handlers
# -----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)

    keyboard = [["📋 Today's Jobs"], ["📞 Contact", "ℹ️ About"], ["💬 Ask AI", "🔍 Search Job"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!",
        reply_markup=reply_markup
    )

async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Today's Jobs:\n\n• Job 1\n• Job 2")

async def search_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_premium(user_id):
        await update.message.reply_text("❌ This feature is only for Premium users.")
        return
    await update.message.reply_text("🔍 Please send your search keyword.")

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_premium(user_id):
        if get_messages_used(user_id) >= 10:
            await update.message.reply_text("⚠️ Free users can use only 10 AI messages per day. Upgrade to Premium.")
            return
    increment_messages(user_id)
    await update.message.reply_text("🤖 AI Response: Hello from AI!")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 Unauthorized.")
        return

    total = total_users()
    premium = premium_users()

    await update.message.reply_text(f"""
👮 Admin Panel:
👥 Total Users: {total}
💎 Premium Users: {premium}
    """)

# -----------------------------
# Start Bot
# -----------------------------
if __name__ == "__main__":
    init_db()
    keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", jobs))
    app.add_handler(CommandHandler("search", search_job))
    app.add_handler(CommandHandler("ask", ask_ai))
    app.add_handler(CommandHandler("admin", admin))

    app.run_polling()
