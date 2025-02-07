from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import csv
from datetime import datetime
from zoneinfo import ZoneInfo  # Para Python 3.9+
import os

# Define tu zona horaria
zona_horaria = ZoneInfo('America/Mexico_City')  # Cambia esto a tu zona horaria

# Accede al token desde las variables de entorno
TOKEN = os.getenv('TOKEN')

data_file = 'bus_data.csv'

# Inicializa el archivo CSV si no existe
if not os.path.exists(data_file):
    with open(data_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Fecha', 'Hora', 'Tipo'])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Bus Subida", callback_data='subida')],
        [InlineKeyboardButton("Bus Bajada", callback_data='bajada')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Selecciona una opción:', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tipo = 'Subida' if query.data == 'subida' else 'Bajada'
    now = datetime.now(zona_horaria)  # Usa la zona horaria definida
    fecha = now.strftime('%Y-%m-%d')
    hora = now.strftime('%H:%M:%S')

    # Guarda los datos en el archivo CSV
    with open(data_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([fecha, hora, tipo])

    # Muestra un mensaje de confirmación
    await query.edit_message_text(text=f"Registrado: {tipo} a las {hora}")

    # Vuelve a mostrar los botones persistentes
    keyboard = [
        [InlineKeyboardButton("Bus Subida", callback_data='subida')],
        [InlineKeyboardButton("Bus Bajada", callback_data='bajada')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('Selecciona una opción:', reply_markup=reply_markup)

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Envía el archivo CSV al usuario
    await update.message.reply_document(document=open(data_file, 'rb'))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler('descargar', descargar))

app.run_polling()
