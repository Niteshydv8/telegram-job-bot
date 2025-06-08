from flask import Flask
from threading import Thread
import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)

# --- Flask for Render Keep-Alive ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "🤖 Bot is alive and running!"

def run():
    web_app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Logging ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# --- Load from environment (Render Secret) ---
BOT_TOKEN = os.environ['TELEGRAM_TOKEN']
ADMIN_ID = 5762701937  # Replace with your real Telegram ID
premium_users = [ADMIN_ID]  # Add premium users here

# --- Bot Commands ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📋 Today's Jobs", "🔍 Search"],
        ["ℹ️ About", "📞 Contact"],
        ["💬 Ask AI 🤖", "👨‍💻 Admin"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"👋 Welcome {update.effective_user.first_name}! Choose an option:",
        reply_markup=reply_markup
    )

async def todays_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Today's Jobs:\n\n• Web Developer at XYZ\n• Graphic Designer at ABC\n• Marketing Intern at MNO"
    )

async def search_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in premium_users:
        await update.message.reply_text("🚫 Only Premium users can use this feature.")
        return
    await update.message.reply_text("🔍 Send a keyword to search jobs (e.g., 'Python').")

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in premium_users:
        await update.message.reply_text("💡 AI Chat is available for Premium users only.")
        return
    await update.message.reply_text("🤖 Ask your question! (This is a test response)")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *About Us*\n\nNepal Job Bot helps you find daily job updates from top Nepali job portals. "
        "Premium users get advanced search and AI assistant.\n\nMade with ❤️ by @Meowamz",
        parse_mode='Markdown'
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Contact us at: support@nepaljobbot.com")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return
    await update.message.reply_text(
        f"👨‍💻 Admin Panel\n\nTotal Users: 123\nPremium Users: {len(premium_users)}"
    )

# --- Main ---
if __name__ == "__main__":
    keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", todays_jobs))
    app.add_handler(CommandHandler("search", search_job))
    app.add_handler(CommandHandler("ask", ask_ai))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("admin", admin))

    # Optional: Handle text button clicks (keyboard)
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Today's Jobs"), todays_jobs))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Search"), search_job))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("About"), about))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Contact"), contact))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Ask AI"), ask_ai))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Admin"), admin))

    app.run_polling()
