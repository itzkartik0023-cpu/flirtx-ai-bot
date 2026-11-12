import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "नमस्ते! मैं FlirtX AI हूँ ❤️\nमुझसे हिंदी या English में बात करो!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent?key=" + GEMINI_API_KEY
    )

    prompt = (
        "You are FlirtX AI, a friendly and respectful Hindi-English "
        "chat assistant. Give fun, kind, age-appropriate conversation "
        "suggestions. Never use sexual content or pressure anyone.\n\n"
        + message
    )

    try:
        response = requests.post(
            url,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30
        )
        data = response.json()
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        answer = "अभी जवाब नहीं मिल पाया। थोड़ी देर बाद कोशिश करो।"

    await update.message.reply_text(answer)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
