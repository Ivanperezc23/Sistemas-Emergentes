import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot musical.")

# Mensajes comunes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Recibí tu mensaje: " + update.message.text)

# Función principal
async def main():
    app = ApplicationBuilder().token("TU_TOKEN_AQUI").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot iniciado...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

