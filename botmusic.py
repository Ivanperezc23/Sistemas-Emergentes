from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yt_dlp
import threading

def start(update, context):
    update.message.reply_text("🎧 ¡Hola! Envíame el nombre de una canción o artista y te enviaré el audio en MP3.")

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

def handle_message(update, context):
    query = update.message.text
    update.message.reply_text(f"🔍 Buscando: {query}...")

    try:
        filename, title = download_mp3(query)
        with open(filename, 'rb') as f:
            update.message.reply_audio(f, title=title)
        os.remove(filename)
    except Exception as e:
        update.message.reply_text("❌ Hubo un error descargando el audio.")
        print(e)

def run_bot():
    TOKEN = "8452976350:AAENIzUCMKfKnFh0ixvWtQFCp45nLe_Yf3Y"  # 🔁 ← Pega aquí tu token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("🎵 Bot de música activo...")
    updater.idle()

# Ejecutar en hilo separado para que no se congele Colab
thread = threading.Thread(target=run_bot)
thread.start()