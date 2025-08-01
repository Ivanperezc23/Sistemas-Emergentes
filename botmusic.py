import asyncio
import os
import uuid
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Función para descargar música
def descargar_musica_mp3(query: str) -> str:
    unique_id = str(uuid.uuid4())
    output_template = f"{unique_id}.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'default_search': 'ytsearch1'
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        return filename

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 ¡Hola! Envíame el nombre de una canción o artista y te enviaré el MP3.")

# Buscar y enviar música
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    chat_id = update.message.chat_id

    msg = await update.message.reply_text("🔍 Buscando tu canción, espera un momento...")

    try:
        mp3_file = descargar_musica_mp3(query)
        await context.bot.send_audio(chat_id=chat_id, audio=open(mp3_file, 'rb'), title=query)
        os.remove(mp3_file)  # Borrar archivo después de enviarlo
        await msg.delete()
    except Exception as e:
        await update.message.reply_text(f"❌ Error al descargar la canción: {str(e)}")

# Ejecutar el bot
async def main():
    app = ApplicationBuilder().token("8452976350:AAENIzUCMKfKnFh0ixvWtQFCp45nLe_Yf3Y").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🎶 Bot musical activo...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
