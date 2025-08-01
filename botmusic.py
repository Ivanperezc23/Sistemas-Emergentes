from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, JobQueue
)
import os
from pytz import timezone
import yt_dlp

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎧 ¡Hola! Envíame el nombre de una canción o artista y te enviaré el audio en MP3.")

def download_mp3(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        title = info['entries'][0]['title']
        return 'audio.mp3', title

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"🔍 Buscando: {query}...")

    try:
        filename, title = download_mp3(query)
        with open(filename, 'rb') as f:
            await update.message.reply_audio(f, title=title)
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text("❌ Error descargando el audio.")
        print("Error:", e)

async def main():
    job_queue = JobQueue(timezone=timezone("UTC"))
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).job_queue(job_queue).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🎵 Bot activo...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

