from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp, os
import google.generativeai as genai
from gtts import gTTS

TOKEN = os.getenv("8232345435:AAG-vN7eVuH8H_ST92XFeKTvBICpXSSZIaQ")
genai.configure(api_key=os.getenv("AIzaSyBqBatEAqsBWMzfIQ65aqT3YeCEY9gAbJ0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Send /play songname | 🤖 /ai message")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    ydl_opts = {'format': 'bestaudio'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        url = info['entries'][0]['url']
    await update.message.reply_audio(audio=url)

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(" ".join(context.args))
    await update.message.reply_text(response.text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("play", play))
app.add_handler(CommandHandler("ai", ai))

app.run_polling()
