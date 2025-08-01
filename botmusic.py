import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎧 ¡Hola! Envíame el nombre de una canción o artista y te enviaré el audio en MP3.")

def download_mp3(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'cookiefile': 'cookies.txt',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            title = info['entries'][0]['title']
            return 'audio.mp3', title
    except Exception as e:
        print("❌ Error en yt_dlp:", e)
        return None, None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"🔍 Buscando: {query}...")

    filename, title = download_mp3(query)
    if not filename:
        await update.message.reply_text("❌ No se pudo descargar el audio. Puede estar bloqueado por restricciones de YouTube.")
        return

    try:
        with open(filename, 'rb') as f:
            await update.message.reply_audio(f, title=title)
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text("❌ Error al enviar el audio.")
        print(e)

async def main():
    app = ApplicationBuilder().token("8452976350:AAENIzUCMKfKnFh0ixvWtQFCp45nLe_Yf3Y").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🎵 Bot de música activo...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
