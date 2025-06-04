import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace with your real bot token from BotFather
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

logging.basicConfig(level=logging.INFO)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Today's Jobs"], ["Contact", "About"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Welcome to Nepal Job Alert Bot!\nUse the buttons below to get started.",
        reply_markup=reply_markup,
    )

# Create application and run bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run_polling()