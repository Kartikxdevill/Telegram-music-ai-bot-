from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp, os, threading
import google.generativeai as genai
from flask import Flask

flask_app = Flask(name)

@flask_app.route('/')
def health_check():
    return "Bot is running!", 200

def run_flask():
 variable
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

TOKEN = os.getenv("8232345435:AAGlHZCx078kNhWJes1ECaGyj7S69X0nS5o")
genai.configure(api_key=os.getenv("AIzaSyBqBatEAqsBWMzfIQ65aqT3YeCEY9gAbJ0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Send /play songname | 🤖 /ai message")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a song name!")
        return
    
    ydl_opts = {'format': 'bestaudio', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        url = info['entries'][0]['url']
    await update.message.reply_audio(audio=url)

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    model = genai.GenerativeModel("gemini-2.5-flash") 
    response = model.generate_content(" ".join(context.args))
    await update.message.reply_text(response.text)

if name == "main":
    # Start Flask in a separate thread
    threading.Thread(target=run_flask, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("ai", ai))
    
    print("Bot is starting...")
    app.run_polling()
