import os
import json
from io import BytesIO
from collections import Counter
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from faker import Faker
import asyncio

TOKEN = os.getenv("8439097842:AAEGxjKleyqYDPqzrin3vGMoW9GKLTc2acY")
WEBHOOK_URL = os.getenv("https://saque-7.onrender.com/webhook")

locales = {
    "usa": "en_US",
    "mexico": "es_MX",
    "españa": "es_ES",
    "brasil": "pt_BR",
    "alemania": "de_DE",
    "francia": "fr_FR",
    "italia": "it_IT",
    "japon": "ja_JP",
}

user_locales = {}
user_history = {}
stats_data_generated = 0
stats_countries_used = Counter()

def get_fake_data(locale):
    fake = Faker(locale)
    return {
        "Nombre": fake.name(),
        "Email": fake.email(),
        "Teléfono": fake.phone_number(),
        "Dirección": fake.address(),
        "Tarjeta": fake.credit_card_number(card_type='visa'),
        "Nacimiento": str(fake.date_of_birth()),
        "País": fake.country(),
        "RFC": fake.ssn()
    }

def format_data_text(data: dict) -> str:
    return (
        f"👤 Nombre: {data['Nombre']}\n"
        f"📧 Email: {data['Email']}\n"
        f"📞 Teléfono: {data['Teléfono']}\n"
        f"🏠 Dirección: {data['Dirección']}\n"
        f"💳 Tarjeta: {data['Tarjeta']}\n"
        f"📅 Nacimiento: {data['Nacimiento']}\n"
        f"🌍 País: {data['País']}\n"
        f"🆔 RFC (falso): {data['RFC']}\n\n"
        f"✨ Creado por: @LooKsCrazy0"
    )

def build_main_menu():
    keyboard = [
        [InlineKeyboardButton("🌎 Cambiar país", callback_data="menu_change_country"),
         InlineKeyboardButton("🎲 Generar datos", callback_data="menu_generate_data")],
        [InlineKeyboardButton("❓ Ayuda", callback_data="menu_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

# === Comandos ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Hola {name}, bienvenido al Generador de Datos Falsos.\nUsa el menú abajo para navegar.\n\n✨ Creado por: @LooKsCrazy0",
        reply_markup=build_main_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Usa los comandos /pais, /fake, /nombre, /email, /tarjeta\n✨ Creado por: @LooKsCrazy0")

async def paises(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌎 Países disponibles:\n" + "\n".join(f"• {p.title()}" for p in locales))

async def set_country_locale(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usa: /pais mexico")
        return
    country = context.args[0].lower()
    if country in locales:
        user_locales[update.effective_user.id] = locales[country]
        await update.message.reply_text(f"✅ País seleccionado: {country.title()}")
    else:
        await update.message.reply_text("❌ País no válido. Usa /paises")

async def generate_fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_locales:
        await update.message.reply_text("❗ Usa /pais primero")
        return
    locale = user_locales[uid]
    data = get_fake_data(locale)
    user_history.setdefault(uid, []).append(data)
    global stats_data_generated
    stats_data_generated += 1
    stats_countries_used[locale] += 1
    await update.message.reply_text(format_data_text(data))

async def generate_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_locales:
        await update.message.reply_text("❗ Usa /pais primero")
        return
    name = Faker(user_locales[uid]).name()
    user_history.setdefault(uid, []).append({"Nombre": name})
    await update.message.reply_text(f"👤 Nombre: {name}")

async def generate_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_locales:
        await update.message.reply_text("❗ Usa /pais primero")
        return
    email = Faker(user_locales[uid]).email()
    user_history.setdefault(uid, []).append({"Email": email})
    await update.message.reply_text(f"📧 Email: {email}")

async def generate_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_locales:
        await update.message.reply_text("❗ Usa /pais primero")
        return
    card = Faker(user_locales[uid]).credit_card_number(card_type='visa')
    user_history.setdefault(uid, []).append({"Tarjeta": card})
    await update.message.reply_text(f"💳 Tarjeta: {card}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("Usa los comandos disponibles por ahora.")

# === MAIN ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("paises", paises))
    app.add_handler(CommandHandler("pais", set_country_locale))
    app.add_handler(CommandHandler("fake", generate_fake))
    app.add_handler(CommandHandler("nombre", generate_name))
    app.add_handler(CommandHandler("email", generate_email))
    app.add_handler(CommandHandler("tarjeta", generate_card))
    app.add_handler(CallbackQueryHandler(button_handler))

    asyncio.run(app.bot.set_webhook(url=WEBHOOK_URL))
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    main()
