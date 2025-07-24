from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from faker import Faker
from datetime import datetime
import logging
import os

TOKEN = os.getenv("8439097842:AAEGxjKleyqYDPqzrin3vGMoW9GKLTc2acY")  # Se recomienda usar variables de entorno

locales = {
    "usa": "en_US",
    "mexico": "es_MX",
    "españa": "es_ES",
    "brasil": "pt_BR",
    "alemania": "de_DE",
    "francia": "fr_FR",
    "italia": "it_IT",
    "japon": "ja_JP"
}

user_locales = {}
historial_cmd = []
stats_data_generated = 0
stats_countries_used = {}

# Banner bonito en consola
print("🧪 𝗕𝗢𝗧 𝗙𝗔𝗞𝗘 𝗗𝗔𝗧𝗔 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥")
print("🎨 By @LooKsCrazy0\n")

# Configurar logs
logging.basicConfig(level=logging.INFO)


def get_fake_data(locale):
    fake = Faker(locale)
    return (
        f"👤 Nombre: {fake.name()}\n"
        f"📧 Email: {fake.email()}\n"
        f"📞 Teléfono: {fake.phone_number()}\n"
        f"🏠 Dirección: {fake.address()}\n"
        f"💳 Tarjeta: {fake.credit_card_number(card_type='visa')}\n"
        f"📅 Nacimiento: {fake.date_of_birth()}\n"
        f"🌍 País: {fake.country()}\n"
        f"🆔 ID Falso: {fake.ssn()}"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🌍 Elegir País", callback_data='paises')],
        [InlineKeyboardButton("📊 Estadísticas", callback_data='stats')],
        [InlineKeyboardButton("📜 Comandos", callback_data='comandos')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 ¡Hola {user.first_name}! Bienvenido a 🧪 𝗙𝗮𝗸𝗲 𝗗𝗮𝘁𝗮 𝗕𝗼𝘁\n"
        f"🎨 Creador: @LooKsCrazy0\n\n"
        f"Selecciona una opción abajo 👇",
        reply_markup=reply_markup
    )


async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(
        "📜 *Comandos Disponibles:*\n"
        "/start - Inicia el bot\n"
        "/pais [nombre] - Establece el país\n"
        "/fake - Genera datos falsos\n"
        "/historial - Ver historial de comandos\n"
        "/stats - Ver estadísticas",
        parse_mode="Markdown"
    )


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated, stats_countries_used
    msg = f"📊 *Estadísticas del Bot:*\n"
    msg += f"• Datos generados: {stats_data_generated}\n"
    msg += "• Países más usados:\n"
    for pais, count in stats_countries_used.items():
        msg += f"   - {pais.title()}: {count} veces\n"
    await update.callback_query.message.reply_text(msg, parse_mode="Markdown")


async def paises(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🌎 *Países disponibles:*\n"
    msg += "\n".join([f"• {p.title()}" for p in locales])
    msg += "\n\nUsa /pais [nombre] para elegir uno."
    await update.callback_query.message.reply_text(msg, parse_mode="Markdown")


async def set_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❗ Usa /pais [nombre]. Ejemplo: /pais mexico")
        return

    country = context.args[0].lower()
    if country in locales:
        user_locales[update.effective_user.id] = locales[country]
        stats_countries_used[country] = stats_countries_used.get(country, 0) + 1
        await update.message.reply_text(f"✅ País establecido a: {country.title()}")
    else:
        await update.message.reply_text("❌ País no válido. Usa /paises para ver la lista.")


async def fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated
    user_id = update.effective_user.id
    locale = user_locales.get(user_id, "en_US")
    stats_data_generated += 1
    data = get_fake_data(locale)
    historial_cmd.append((user_id, "fake", datetime.now().isoformat()))
    await update.message.reply_text(data)


async def historial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_history = [h for h in historial_cmd if h[0] == user_id]
    if not user_history:
        await update.message.reply_text("📭 No tienes historial aún.")
        return
    msg = "📜 *Tu Historial de Comandos:*\n"
    for _, cmd, date in user_history[-5:]:
        msg += f"• /{cmd} — {date}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")


async def inline_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "paises":
        await paises(update, context)
    elif data == "stats":
        await show_stats(update, context)
    elif data == "comandos":
        await comandos(update, context)


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fake", fake))
    app.add_handler(CommandHandler("pais", set_country))
    app.add_handler(CommandHandler("historial", historial))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(CallbackQueryHandler(inline_callback))

    app.run_polling()
