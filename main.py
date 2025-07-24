import os
import json
from io import BytesIO
from collections import Counter
from faker import Faker
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Banner en consola
def print_banner():
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    banner = f"""
{CYAN}===============================================
{GREEN}   ██████▄  █████▄  █████▄ █████▇█████▇
   ██╔═██║██╔═══██║██╔═══╝ ██╔═══╝
   ██████╗╝██║   ██║██║  ████▃  ████▃  
   ██╔═══╝ ██║   ██║██║   ██║██╔═╝  ██╔═╝  
   ██║     ╚█████╔╝╚█████╔╝█████▇█████▇
   ╚╝      ╚╝╚╝╚╝  ╚╝╚╝  ╚╝ ╚╝╚╝  ╚╝╚╝  ╚╝{YELLOW}

     Generador de Datos Falsos - Bot de Telegram
           Creado por: @LooKsCrazy0
{CYAN}===============================================

{RESET}"""
    print(banner)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ No se encontró la variable BOT_TOKEN. Por favor configúrala en Render.")

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

# Funciones principales

def get_fake_data(locale):
    fake = Faker(locale)
    data = {
        "Nombre": fake.name(),
        "Email": fake.email(),
        "Teléfono": fake.phone_number(),
        "Dirección": fake.address(),
        "Tarjeta": fake.credit_card_number(card_type='visa'),
        "Nacimiento": str(fake.date_of_birth()),
        "País": fake.country(),
        "RFC": fake.ssn()
    }
    return data

def format_data_text(data):
    return (
        f"👤 Nombre: {data['Nombre']}\n"
        f"📧 Email: {data['Email']}\n"
        f"📞 Teléfono: {data['Teléfono']}\n"
        f"🏠 Dirección: {data['Dirección']}\n"
        f"💳 Tarjeta: {data['Tarjeta']}\n"
        f"📅 Nacimiento: {data['Nacimiento']}\n"
        f"🌍 País: {data['País']}\n"
        f"🆔 RFC (falso): {data['RFC']}\n"
        f"\n✨ Creado por: @LooKsCrazy0"
    )

def build_main_menu():
    keyboard = [
        [InlineKeyboardButton("🌎 Cambiar país", callback_data="menu_change_country"),
         InlineKeyboardButton("🎲 Generar datos", callback_data="menu_generate_data")],
        [InlineKeyboardButton("📜 Ver historial", callback_data="menu_show_history"),
         InlineKeyboardButton("📊 Estadísticas", callback_data="menu_stats")],
        [InlineKeyboardButton("❓ Ayuda", callback_data="menu_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Handlers async
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_locales[user.id] = "es_MX"
    await update.message.reply_text(
        f"👋 Hola {user.first_name}, bienvenido al Generador de Datos Falsos.\nUsa el menú para comenzar.",
        reply_markup=build_main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "menu_generate_data":
        locale = user_locales.get(user_id, "es_MX")
        data = get_fake_data(locale)
        global stats_data_generated
        stats_data_generated += 1
        stats_countries_used[locale] += 1
        user_history.setdefault(user_id, []).append(data)
        await query.edit_message_text(format_data_text(data), reply_markup=build_main_menu())

    elif query.data == "menu_change_country":
        keyboard = [[InlineKeyboardButton(p, callback_data=f"country_{p.lower()}")] for p in locales.keys()]
        await query.edit_message_text("🌍 Elige un país:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("country_"):
        country = query.data.split("_")[1]
        if country in locales:
            user_locales[user_id] = locales[country]
            await query.edit_message_text(f"✅ País cambiado a {country.capitalize()}.", reply_markup=build_main_menu())

    elif query.data == "menu_show_history":
        history = user_history.get(user_id, [])
        if not history:
            await query.edit_message_text("📜 No tienes historial.", reply_markup=build_main_menu())
            return
        json_data = json.dumps(history, indent=2, ensure_ascii=False)
        file = BytesIO(json_data.encode("utf-8"))
        file.name = "historial.json"
        await context.bot.send_document(chat_id=query.message.chat.id, document=InputFile(file))
        await query.edit_message_text("📤 Historial enviado como archivo.", reply_markup=build_main_menu())

    elif query.data == "menu_stats":
        stats = f"📊 Datos generados: {stats_data_generated}\n"
        for k, v in stats_countries_used.items():
            stats += f"🌍 {k}: {v}\n"
        await query.edit_message_text(stats, reply_markup=build_main_menu())

    elif query.data == "menu_help":
        help_text = (
            "❓ *Ayuda del Bot*\n\n"
            "- Usa el botón 'Cambiar país' para seleccionar la región de los datos.\n"
            "- 'Generar datos' te creará un conjunto de información falsa.\n"
            "- Puedes revisar tu historial o ver estadísticas del bot.\n\n"
            "✨ Creado por: @LooKsCrazy0"
        )
        await query.edit_message_text(help_text, reply_markup=build_main_menu(), parse_mode="Markdown")

# Main
def main():
    print_banner()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("[INFO] Bot iniciado.")
    app.run_polling()

if __name__ == '__main__':
    main()
