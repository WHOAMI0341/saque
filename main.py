import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from faker import Faker

TOKEN = os.getenv("8439097842:AAEGxjKleyqYDPqzrin3vGMoW9GKLTc2acY")

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
stats_data_generated = 0
stats_countries_used = {}

def get_fake_data(locale):
    fake = Faker(locale)
    return (
        f"👤 Nombre: {fake.name()}
"
        f"📧 Email: {fake.email()}
"
        f"📞 Teléfono: {fake.phone_number()}
"
        f"🏠 Dirección: {fake.address()}
"
        f"💳 Tarjeta: {fake.credit_card_number(card_type='visa')}
"
        f"📅 Nacimiento: {fake.date_of_birth()}
"
        f"🌍 País: {fake.country()}
"
        f"🆔 ID (falso): {fake.ssn()}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    banner = (
        "🧪 𝗕𝗢𝗧 𝗙𝗔𝗞𝗘 𝗗𝗔𝗧𝗔 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥
"
        "🎨 By @LooKsCrazy0

"
        "Usa /comandos para ver lo que puedo hacer 💡"
    )
    await update.message.reply_text(banner)

async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton("🌎 Seleccionar País", callback_data='menu_paises')],
               [InlineKeyboardButton("📊 Ver Estadísticas", callback_data='menu_stats')],
               [InlineKeyboardButton("💾 Generar Datos", callback_data='menu_fake')]]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("✨ Elige una opción:", reply_markup=markup)

async def pais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🌎 Países disponibles:
"
    msg += "
".join([f"• {p.title()}" for p in locales])
    msg += "

Usa el comando así:
/pais mexico"
    await update.message.reply_text(msg)

async def pais_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❗ Usa el comando así: /pais mexico")
        return
    global stats_countries_used
    country = context.args[0].lower()
    if country in locales:
        user_locales[update.effective_user.id] = locales[country]
        stats_countries_used[country] = stats_countries_used.get(country, 0) + 1
        await update.message.reply_text(f"✅ País seleccionado: {country.title()}")
    else:
        await update.message.reply_text("❌ País no válido. Usa /paises para ver la lista.")

async def fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated
    user_id = update.effective_user.id
    locale = user_locales.get(user_id, "en_US")
    stats_data_generated += 1
    await update.message.reply_text(get_fake_data(locale))

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"📈 Datos generados: {stats_data_generated}
"
    msg += "🌍 Países usados:
"
    for k, v in stats_countries_used.items():
        msg += f"• {k.title()}: {v} veces
"
    await update.message.reply_text(msg or "No hay estadísticas aún.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("comandos", comandos))
    app.add_handler(CommandHandler("fake", fake))
    app.add_handler(CommandHandler("pais", pais_set))
    app.add_handler(CommandHandler("paises", pais))
    app.add_handler(CommandHandler("stats", stats))
    print("🤖 Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
