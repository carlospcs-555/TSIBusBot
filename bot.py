from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import pandas as pd
from datetime import datetime
import os

# Reemplaza 'YOUR_TELEGRAM_BOT_TOKEN' con el token de tu bot
TOKEN = '7863553522:AAF8TowMqtghdoWtYUK--7Oazf94_PNSGVA'

data_file = 'bus_data.xlsx'

# Inicializa el archivo Excel si no existe
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=['Fecha', 'Hora', 'Tipo'])
    df.to_excel(data_file, index=False)

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
    now = datetime.now()
    fecha = now.strftime('%Y-%m-%d')
    hora = now.strftime('%H:%M:%S')

    # Guarda los datos en Excel
    df = pd.read_excel(data_file)
    df = pd.concat([df, pd.DataFrame([[fecha, hora, tipo]], columns=['Fecha', 'Hora', 'Tipo'])], ignore_index=True)
    df.to_excel(data_file, index=False)

    '''await query.edit_message_text(text=f"Registrado: {tipo} a las {hora}")'''

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_document(document=open(data_file, 'rb'))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler('descargar', descargar))

app.run_polling()
