from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from faker import Faker

TOKEN = "8439097842:AAEGxjKleyqYDPqzrin3vGMoW9GKLTc2acY"

BANNER = (
    "🧪 𝗕𝗢𝗧 𝗙𝗔𝗞𝗘 𝗗𝗔𝗧𝗔 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥\n"
    "🎨 By @LooKsCrazy0\n"
    "🛠 /comandos para ayuda | /paises para ver países disponibles\n"
)

# 🌍 Diccionario de países soportados
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

# 🔄 Estado por usuario
user_locales = {}

# 📊 Estadísticas
stats_data_generated = 0
stats_countries_used = {key: 0 for key in locales}

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

# 🟢 Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"{BANNER}\n👋 ¡Hola, {user}! Usa /comandos para ver lo que puedo hacer."
    )

# 🌎 Comando /paises
async def show_countries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🌐 Países disponibles:\n"
    msg += "\n".join([f"• {p.title()}" for p in locales])
    msg += "\n\nUsa el comando así:\n/pais mexico"
    await update.message.reply_text(msg)

# 🧭 Comando /pais
async def set_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_countries_used
    if len(context.args) == 0:
        await update.message.reply_text("❗ Usa el comando así: /pais mexico")
        return

    country = context.args[0].lower()
    if country in locales:
        user_locales[update.effective_user.id] = locales[country]
        stats_countries_used[country] += 1
        await update.message.reply_text(f"✅ País seleccionado: {country.title()}")
    else:
        await update.message.reply_text("❌ País no válido. Usa /paises para ver la lista.")

# 📊 Comando /estadisticas
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"📈 Estadísticas de uso:\n"
    msg += f"🔢 Datos generados: {stats_data_generated}\n"
    msg += "🌍 Países más usados:\n"
    for country, count in stats_countries_used.items():
        if count > 0:
            msg += f"• {country.title()}: {count}\n"
    await update.message.reply_text(msg)

# 📋 Comando /comandos
async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Comandos disponibles:\n"
        "/start - Inicia el bot\n"
        "/paises - Muestra países disponibles\n"
        "/pais <nombre> - Selecciona país para datos\n"
        "/fake - Genera datos falsos\n"
        "/estadisticas - Muestra estadísticas\n"
        "/comandos - Muestra este menú"
    )

# 🎭 Comando /fake
async def generate_fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated
    user_id = update.effective_user.id
    locale = user_locales.get(user_id, "en_US")
    data = get_fake_data(locale)
    stats_data_generated += 1
    await update.message.reply_text(data)

# 🔁 Inicia el bot
if __name__ == "__main__":
    print(BANNER)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paises", show_countries))
    app.add_handler(CommandHandler("pais", set_country))
    app.add_handler(CommandHandler("fake", generate_fake))
    app.add_handler(CommandHandler("estadisticas", stats))
    app.add_handler(CommandHandler("comandos", comandos))
    app.run_polling()
