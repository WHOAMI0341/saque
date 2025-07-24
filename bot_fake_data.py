import json
from io import BytesIO
from collections import Counter
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
from faker import Faker
import os

# --- Banner y colores para consola ---
def print_banner():
    RED = "\033[91m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    banner = f"""
{CYAN}===============================================
{GREEN}   ██████╗  ██████╗  ██████╗ ███████╗███████╗
   ██╔══██╗██╔═══██╗██╔════╝ ██╔════╝██╔════╝
   ██████╔╝██║   ██║██║  ███╗█████╗  █████╗  
   ██╔═══╝ ██║   ██║██║   ██║██╔══╝  ██╔══╝  
   ██║     ╚██████╔╝╚██████╔╝███████╗███████╗
   ╚═╝      ╚═════╝  ╚═════╝ ╚══════╝╚══════╝{YELLOW}

     Generador de Datos Falsos - Bot Telegram
           Creado por: @LooKsCrazy0
{CYAN}===============================================

{RESET}"""
    print(banner)

# TOKEN desde variable de entorno
TOKEN = os.getenv("TOKEN")

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
        [
            InlineKeyboardButton("🌎 Cambiar país", callback_data="menu_change_country"),
            InlineKeyboardButton("🎲 Generar datos", callback_data="menu_generate_data"),
        ],
        [
            InlineKeyboardButton("📜 Ver historial", callback_data="menu_show_history"),
            InlineKeyboardButton("📊 Estadísticas", callback_data="menu_stats"),
        ],
        [
            InlineKeyboardButton("❓ Ayuda", callback_data="menu_help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    welcome_text = (
        f"👋 Hola {user_first_name}, bienvenido al Generador de Datos Falsos.\n\n"
        "Usa el menú de abajo para navegar entre opciones.\n\n"
        "✨ Creado por: @LooKsCrazy0"
    )
    await update.message.reply_text(welcome_text, reply_markup=build_main_menu())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 *Comandos disponibles:*\n\n"
        "/start - Iniciar el bot y mostrar menú\n"
        "/paises - Mostrar lista de países disponibles\n"
        "/pais <nombre> - Seleccionar país (ejemplo: /pais mexico)\n"
        "/fake - Generar datos falsos según el país seleccionado\n"
        "/nombre - Generar solo un nombre falso\n"
        "/email - Generar solo un email falso\n"
        "/tarjeta - Generar solo una tarjeta de crédito falsa\n"
        "/historial - Ver tus últimos datos generados\n"
        "/exportar_txt - Exportar tu historial en archivo TXT\n"
        "/exportar_json - Exportar tu historial en archivo JSON\n"
        "/help - Mostrar este mensaje de ayuda\n\n"
        "✨ Creado por: @LooKsCrazy0"
    )
    await update.message.reply_text(help_text)

async def paises(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🌎 Países disponibles:\n"
    msg += "\n".join([f"• {p.title()}" for p in locales])
    msg += "\n\n✨ Creado por: @LooKsCrazy0"
    await update.message.reply_text(msg)

async def set_country_locale(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❗ Usa el comando así: /pais mexico\n\n✨ Creado por: @LooKsCrazy0")
        return

    country = context.args[0].lower()
    if country in locales:
        user_locales[update.effective_user.id] = locales[country]
        await update.message.reply_text(f"✅ País seleccionado: {country.title()}\n\n✨ Creado por: @LooKsCrazy0")
    else:
        await update.message.reply_text("❌ País no válido. Usa /paises para ver la lista.\n\n✨ Creado por: @LooKsCrazy0")

async def generate_fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated, stats_countries_used
    user_id = update.effective_user.id
    if user_id not in user_locales:
        await update.message.reply_text("❗ Por favor selecciona un país primero usando /pais <nombre>\n\n✨ Creado por: @LooKsCrazy0")
        return

    locale = user_locales[user_id]
    data = get_fake_data(locale)
    text = format_data_text(data)

    user_history.setdefault(user_id, []).append(data)
    stats_data_generated += 1
    stats_countries_used[locale] += 1

    await update.message.reply_text(text)

async def generate_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated, stats_countries_used
    user_id = update.effective_user.id
    if user_id not in user_locales:
        await update.message.reply_text("❗ Por favor selecciona un país primero usando /pais <nombre>\n\n✨ Creado por: @LooKsCrazy0")
        return
    locale = user_locales[user_id]
    name = Faker(locale).name()
    user_history.setdefault(user_id, []).append({"Nombre": name})
    stats_data_generated += 1
    stats_countries_used[locale] += 1
    await update.message.reply_text(f"👤 Nombre falso:\n{name}\n\n✨ Creado por: @LooKsCrazy0")

async def generate_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated, stats_countries_used
    user_id = update.effective_user.id
    if user_id not in user_locales:
        await update.message.reply_text("❗ Por favor selecciona un país primero usando /pais <nombre>\n\n✨ Creado por: @LooKsCrazy0")
        return
    locale = user_locales[user_id]
    email = Faker(locale).email()
    user_history.setdefault(user_id, []).append({"Email": email})
    stats_data_generated += 1
    stats_countries_used[locale] += 1
    await update.message.reply_text(f"📧 Email falso:\n{email}\n\n✨ Creado por: @LooKsCrazy0")

async def generate_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stats_data_generated, stats_countries_used
    user_id = update.effective_user.id
    if user_id not in user_locales:
        await update.message.reply_text("❗ Por favor selecciona un país primero usando /pais <nombre>\n\n✨ Creado por: @LooKsCrazy0")
        return
    locale = user_locales[user_id]
    card = Faker(locale).credit_card_number(card_type='visa')
    user_history.setdefault(user_id, []).append({"Tarjeta": card})
    stats_data_generated += 1
    stats_countries_used[locale] += 1
    await update.message.reply_text(f"💳 Tarjeta de crédito falsa:\n{card}\n\n✨ Creado por: @LooKsCrazy0")

async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    history = user_history.get(user_id)
    if not history:
        await update.message.reply_text("No tienes datos generados aún.\n\n✨ Creado por: @LooKsCrazy0")
        return
    lines = []
    for i, entry in enumerate(history[-10:], start=1):
        line = f"{i}. " + ", ".join(f"{k}: {v}" for k, v in entry.items())
        lines.append(line)
    await update.message.reply_text("📜 *Tu historial de datos recientes:*\n" + "\n".join(lines) + "\n\n✨ Creado por: @LooKsCrazy0", parse_mode="Markdown")

async def export_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    history = user_history.get(user_id)
    if not history:
        await update.message.reply_text("No tienes datos generados aún para exportar.\n\n✨ Creado por: @LooKsCrazy0")
        return
    txt_data = ""
    for i, entry in enumerate(history, start=1):
        txt_data += f"{i}.\n"
        for k, v in entry.items():
            txt_data += f"{k}: {v}\n"
        txt_data += "\n"
    bio = BytesIO()
    bio.write(txt_data.encode("utf-8"))
    bio.seek(0)
    await update.message.reply_document(document=InputFile(bio, filename="historial.txt"), caption="Aquí tienes tu historial en TXT\n\n✨ Creado por: @LooKsCrazy0")

async def export_json(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    history = user_history.get(user_id)
    if not history:
        await update.message.reply_text("No tienes datos generados aún para exportar.\n\n✨ Creado por: @LooKsCrazy0")
        return
    json_data = json.dumps(history, ensure_ascii=False, indent=2)
    bio = BytesIO()
    bio.write(json_data.encode("utf-8"))
    bio.seek(0)
    await update.message.reply_document(document=InputFile(bio, filename="historial.json"), caption="Aquí tienes tu historial en JSON\n\n✨ Creado por: @LooKsCrazy0")

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = stats_data_generated
    most_used = stats_countries_used.most_common(3)
    msg = f"📊 *Estadísticas del bot:*\n\nTotal datos generados: {total}\n\nPaíses más usados:\n"
    if most_used:
        for country, count in most_used:
            readable_country = next((k.title() for k,v in locales.items() if v == country), country)
            msg += f"• {readable_country}: {count}\n"
    else:
        msg += "Ningún dato generado aún."
    msg += "\n\n✨ Creado por: @LooKsCrazy0"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "menu_change_country":
        keyboard = []
        keys = list(locales.keys())
        for i in range(0, len(keys), 3):
            row = [
                InlineKeyboardButton(keys[j].title(), callback_data=f"set_country_{keys[j]}")
                for j in range(i, min(i+3, len(keys)))
            ]
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("⬅️ Volver", callback_data="menu_main")])
        await query.edit_message_text("🌎 Selecciona un país:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "menu_generate_data":
        keyboard = [
            [InlineKeyboardButton("Generar datos completos", callback_data="gen_full")],
            [
                InlineKeyboardButton("Solo nombre", callback_data="gen_name"),
                InlineKeyboardButton("Solo email", callback_data="gen_email"),
                InlineKeyboardButton("Solo tarjeta", callback_data="gen_card"),
            ],
            [InlineKeyboardButton("⬅️ Volver", callback_data="menu_main")],
        ]
        await query.edit_message_text("🎲 Elige qué tipo de datos generar:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "menu_show_history":
        history = user_history.get(user_id)
        if not history:
            await query.answer("No tienes datos generados aún.", show_alert=True)
            return
        lines = []
        for i, entry in enumerate(history[-10:], start=1):
            line = f"{i}. " + ", ".join(f"{k}: {v}" for k, v in entry.items())
            lines.append(line)
        await query.edit_message_text("📜 *Tu historial de datos recientes:*\n" + "\n".join(lines) + "\n\n✨ Creado por: @LooKsCrazy0", parse_mode="Markdown")

    elif data == "menu_stats":
        total = stats_data_generated
        most_used = stats_countries_used.most_common(3)
        msg = f"📊 *Estadísticas del bot:*\n\nTotal datos generados: {total}\n\nPaíses más usados:\n"
        if most_used:
            for country, count in most_used:
                readable_country = next((k.title() for k,v in locales.items() if v == country), country)
                msg += f"• {readable_country}: {count}\n"
        else:
            msg += "Ningún dato generado aún."
        msg += "\n\n✨ Creado por: @LooKsCrazy0"
        await query.edit_message_text(msg, parse_mode="Markdown")

    elif data == "menu_help":
        help_text = (
            "🛠 *Comandos disponibles:*\n\n"
            "/start - Iniciar el bot y mostrar menú\n"
            "/paises - Mostrar lista de países disponibles\n"
            "/pais <nombre> - Seleccionar país (ejemplo: /pais mexico)\n"
            "/fake - Generar datos falsos según el país seleccionado\n"
            "/nombre - Generar solo un nombre falso\n"
            "/email - Generar solo un email falso\n"
            "/tarjeta - Generar solo una tarjeta de crédito falsa\n"
            "/historial - Ver tus últimos datos generados\n"
            "/exportar_txt - Exportar tu historial en archivo TXT\n"
            "/exportar_json - Exportar tu historial en archivo JSON\n"
            "/help - Mostrar este mensaje de ayuda\n\n"
            "✨ Creado por: @LooKsCrazy0"
        )
        await query.edit_message_text(help_text, parse_mode="Markdown")

    elif data.startswith("set_country_"):
        country_key = data.replace("set_country_", "")
        if country_key in locales:
            user_locales[user_id] = locales[country_key]
            await query.edit_message_text(
                f"✅ País seleccionado: {country_key.title()}\n\nUsa /fake o el menú para generar datos.\n\n✨ Creado por: @LooKsCrazy0",
                reply_markup=build_main_menu(),
            )
        else:
            await query.edit_message_text("❌ País no válido.", reply_markup=build_main_menu())

    elif data == "gen_full":
        global stats_data_generated, stats_countries_used
        if user_id not in user_locales:
            await query.answer("Por favor selecciona un país primero usando el menú o /pais", show_alert=True)
            return
        locale = user_locales[user_id]
        data = get_fake_data(locale)
        user_history.setdefault(user_id, []).append(data)
        stats_data_generated += 1
        stats_countries_used[locale] += 1
        text = format_data_text(data)
        await query.edit_message_text(text, reply_markup=build_main_menu())

    elif data == "gen_name":
        global stats_data_generated, stats_countries_used
        if user_id not in user_locales:
            await query.answer("Por favor selecciona un país primero usando el menú o /pais", show_alert=True)
            return
        locale = user_locales[user_id]
        name = Faker(locale).name()
        user_history.setdefault(user_id, []).append({"Nombre": name})
        stats_data_generated += 1
        stats_countries_used[locale] += 1
        await query.edit_message_text(f"👤 Nombre falso:\n{name}\n\n✨ Creado por: @LooKsCrazy0", reply_markup=build_main_menu())

    elif data == "gen_email":
        global stats_data_generated, stats_countries_used
        if user_id not in user_locales:
            await query.answer("Por favor selecciona un país primero usando el menú o /pais", show_alert=True)
            return
        locale = user_locales[user_id]
        email = Faker(locale).email()
        user_history.setdefault(user_id, []).append({"Email": email})
        stats_data_generated += 1
        stats_countries_used[locale] += 1
        await query.edit_message_text(f"📧 Email falso:\n{email}\n\n✨ Creado por: @LooKsCrazy0", reply_markup=build_main_menu())

    elif data == "gen_card":
        global stats_data_generated, stats_countries_used
        if user_id not in user_locales:
            await query.answer("Por favor selecciona un país primero usando el menú o /pais", show_alert=True)
            return
        locale = user_locales[user_id]
        card = Faker(locale).credit_card_number(card_type='visa')
        user_history.setdefault(user_id, []).append({"Tarjeta": card})
        stats_data_generated += 1
        stats_countries_used[locale] += 1
        await query.edit_message_text(f"💳 Tarjeta de crédito falsa:\n{card}\n\n✨ Creado por: @LooKsCrazy0", reply_markup=build_main_menu())

    elif data == "menu_main":
        await query.edit_message_text("Menú principal:", reply_markup=build_main_menu())

    else:
        await query.answer("Acción no reconocida.", show_alert=True)

async def main():
    print_banner()
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("paises", paises))
    application.add_handler(CommandHandler("pais", set_country_locale))
    application.add_handler(CommandHandler("fake", generate_fake))
    application.add_handler(CommandHandler("nombre", generate_name))
    application.add_handler(CommandHandler("email", generate_email))
    application.add_handler(CommandHandler("tarjeta", generate_card))
    application.add_handler(CommandHandler("historial", show_history))
    application.add_handler(CommandHandler("exportar_txt", export_txt))
    application.add_handler(CommandHandler("exportar_json", export_json))
    application.add_handler(CommandHandler("estadisticas", show_stats))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Bot iniciado y listo para usar.")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
