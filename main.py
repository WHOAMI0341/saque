import os
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

# --- Banner y colores ---
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

     Generador de Datos Falsos - Bot de Telegram
           Creado por: @LooKsCrazy0
{CYAN}===============================================

{RESET}"""
    print(banner)

TOKEN = os.getenv("BOT_TOKEN")

locales = {...}  # Recortado por espacio, reemplazar por tu diccionario completo
# El resto del código debe pegarse aquí (puedes copiarlo tú para mantenerlo completo)
# Solo recuerda que el TOKEN ahora viene de os.getenv
