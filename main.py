import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ No se encontró la variable BOT_TOKEN. Por favor configúrala en Render.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Hola {update.effective_user.first_name}, ¡bienvenido!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("[INFO] Bot iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()
