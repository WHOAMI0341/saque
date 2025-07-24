# main.py

import os
from bot_fake_data import (
    print_banner,
    start, help_command, paises, set_country_locale,
    generate_fake, generate_name, generate_email, generate_card,
    historial_cmd, exportar_txt_cmd, exportar_json_cmd,
    button_handler
)
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# Obtener el token desde las variables de entorno
TOKEN = os.getenv("TOKEN")

if __name__ == "__main__":
    print_banner()
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("paises", paises))
    app.add_handler(CommandHandler("pais", set_country_locale))
    app.add_handler(CommandHandler("fake", generate_fake))
    app.add_handler(CommandHandler("nombre", generate_name))
    app.add_handler(CommandHandler("email", generate_email))
    app.add_handler(CommandHandler("tarjeta", generate_card))
    app.add_handler(CommandHandler("historial", historial_cmd))
    app.add_handler(CommandHandler("exportar_txt", exportar_txt_cmd))
    app.add_handler(CommandHandler("exportar_json", exportar_json_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot corriendo...")
    app.run_polling()
