import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp
import google.generativeai as genai

# ================== KEYS (DIRECT) ==================
BOT_TOKEN = "8232345435:AAGlHZCx078kNhWJes1ECaGyj7S69X0nS5o"
GEMINI_API_KEY = "AIzaSyBqBatEAqsBWMzfIQ65aqT3YeCEY9gAbJ0"
# ===================================================

# ---------- Flask (Render health check) ----------
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot is running", 200

def run_flask():
    app_flask.run(host="0.0.0.0", port=10000)

# ---------- Gemini ----------
genai.configure(api_key=GEMINI_API_KEY)

# ---------- Telegram Commands ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Bot Active!\n\n"
        "🎵 /play <song name>\n"
        "🤖 /ai <message>"
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("❌ Song name likho\nExample: /play kesariya")
        return

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            url = info["entries"][0]["url"]

        await update.message.reply_text(f"🎶 Song found:\n{url}")

    except Exception as e:
        await update.message.reply_text("❌ Song error")
        print(e)

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Message likho\nExample: /ai hello")
        return

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(" ".join(context.args))
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("❌ AI error")
        print(e)

# ---------- Main ----------
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("ai", ai))

    print("Bot started successfully...")
    app.run_polling()
