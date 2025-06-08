from flask import Flask
from threading import Thread
import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)

# Flask app to keep bot alive on free hosting
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "🤖 Bot is running!"

def run():
    web_app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Environment token
BOT_TOKEN = os.environ['TELEGRAM_TOKEN']
ADMIN_ID = 5762701937  # Your Telegram ID

# Simulated premium users list (replace with DB later)
premium_users = [ADMIN_ID]

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Today's Jobs"], ["Contact", "About"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"👋 Welcome {update.effective_user.first_name}!",
        reply_markup=reply_markup
    )

# /jobs command
async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Today's Jobs:\n\n• Job 1\n• Job 2")

# /search command
async def search_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in premium_users:
        await update.message.reply_text("❌ This feature is only for Premium users.")
        return
    await update.message.reply_text("🔍 Please send your search keyword.")

# /ask command (AI)
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 AI Answer: This is a sample AI response.")

# /admin command
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return
    await update.message.reply_text(
        "👨‍💻 Admin Panel:\n"
        "- Total Users: 123\n"
        "- Premium Users: 5"
    )

# Initialize and run bot
if __name__ == "__main__":
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", jobs))  # fixed function name
    app.add_handler(CommandHandler("search", search_job))
    app.add_handler(CommandHandler("ask", ask_ai))
    app.add_handler(CommandHandler("admin", admin))
    app.run_polling()
