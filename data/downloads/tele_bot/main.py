from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from bot import run_spreadsheet_task

# Token API Telegram
TELEGRAM_TOKEN = '7473429203:AAH_SA2JlEtIZZfQ9m7ysh0bLgAsduy1exo'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Halo! Gunakan perintah /run_task untuk menjalankan tugas otomatis.')

async def run_task(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Menjalankan tugas otomatis...')
    run_spreadsheet_task()
    await update.message.reply_text('Tugas selesai!')

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('run_task', run_task))

    application.run_polling()

if __name__ == '__main__':
    main() 