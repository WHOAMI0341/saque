from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from faker import Faker
import logging

# Banner
BANNER = """🧪 𝗕𝗢𝗧 𝗙𝗔𝗞𝗘 𝗗𝗔𝗧𝗔 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥
🎨 By @LooKsCrazy0
"""

# Token del bot
TOKEN = "TU_TOKEN_AQUI"  # ← Sustituye con tu token real

# Diccionario de locales por país
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

# Variables globales
user_locales = {}
user_history = {}
stats_data_generated = 0
stats_countries_used = {}

# Obtener datos falsos
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
        f"🆔 RFC (falso): {fake.ssn()}"
    )

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first = update.effective_user.first_name
    keyboard = [
        [InlineKeyboardButton("📄 Ver comandos", callback_data="comandos")],
        [InlineKeyboardButton("🌍 Elegir país", callback_data="pais")],
        [InlineKeyboardButton("🧪 Generar datos", callback_data="fake")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"{BANNER}\n👋 Hola {user_first}, bienvenido al generador de datos falsos.\nUsa los botones o comandos abajo 👇",
        reply_markup=reply_markup
    )

# Botón /callback
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "comandos":
        await help_command(update, context)
    elif query.data == "pais":
        await show_countries(update, context)
    elif query.data == "fake":
        await generate_fake(update, context)

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📜 *Comandos disponibles:*\n"
        "/start - Iniciar el bot\n"
        "/fake - Generar datos falsos\n"
        "/pais <nombre> - Seleccionar país\n"
        "/paises - Lista de países\n"
        "/historial - Ver tu historial\n"
        "/estadisticas - Ver estadísticas globales"
    )
    await update.effective_message.reply_text(msg, parse_mode="Markdown")

# Comando /paises
async def show_countries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🌍 Países disponibles:\n"
    msg += "\n".join([f"• {p.title()}" for p in locales])
    msg += "\n\nUsa /pais <nombre> para seleccionar"
    await update.effective_message.reply_text(msg)

# Comando /pais
async def set_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❗ Usa el comando así: /pais mexico")
        return
    global stats_countries_used
    user_id = update.effective_user.id
    country = context.args[0].lower()
    if country in locales:
        user_locales[user_id] = locales[country]
        stats_countries_used[country] = stats_countries_used.get(country, 0) + 1
        await update.message.reply_text(f"✅ País seleccionado: {country.title()}")
    else:
        await update.message.reply_text("❌ País no válido. Usa /paises para ver la lista.")

# Comando /fake
async def generate_fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated
    user_id = update.effective_user.id
    locale = user_locales.get(user_id, "en_US")
    data = get_fake_data(locale)
    stats_data_generated += 1

    # Guardar historial
    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].append(data)

    await update.effective_message.reply_text(data)

# Comando /historial
async def historial_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    history = user_history.get(user_id, [])
    if not history:
        await update.message.reply_text("📭 No tienes historial todavía.")
    else:
        text = "\n\n".join(history[-5:])
        await update.message.reply_text(f"📜 Últimos datos generados:\n\n{text}")

# Comando /estadisticas
async def estadisticas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated, stats_countries_used
    msg = (
        f"📈 *Estadísticas globales:*\n"
        f"• Datos generados: {stats_data_generated}\n"
        f"• Países usados:\n"
    )
    for pais, count in stats_countries_used.items():
        msg += f"  - {pais.title()}: {count}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

# Iniciar bot
if __name__ == "__main__":
    print(BANNER)
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("paises", show_countries))
    app.add_handler(CommandHandler("pais", set_country))
    app.add_handler(CommandHandler("fake", generate_fake))
    app.add_handler(CommandHandler("historial", historial_cmd))
    app.add_handler(CommandHandler("estadisticas", estadisticas))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()
