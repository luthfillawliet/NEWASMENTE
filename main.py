from ASMENTE import Asmente
from parameter import Parameter
from FILEMANAGER import filemanager
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import requests

pm = Parameter()
fm = filemanager()


def start(update, context):
    query = update.callback_query
    context.bot.send_message(
        chat_id=pm.chat_id, text="Bot Standby...")


def read_command(update, context):
    if (update.message.text[:2] == "ct"):
        # Eksekusi buat CT
        context.bot.send_message(
            chat_id=pm.chat_id, text="Memulai pembuatan CT")
        status, message = Asmente.buatCT(
            id_pelanggan=update.message.text[3:15])
        if (status == "yes"):
            print("STATUS MAIN : ", message)
            context.bot.send_message(chat_id=pm.chat_id, text=message)
            time.sleep(2)
            resp = requests.post(
                "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(pm.chat_id), files=fm.send_photos(pm.files_foto_ct))
        else:
            print("STATUS MAIN : ", message)
            context.bot.send_message(chat_id=pm.chat_id, text=message)
    else:
        print("command tidak dikenal")
        context.bot.send_message(
            chat_id=pm.chat_id, text="command tidak dikenal")


def main():
    # bot Telegram
    # Create updater and pass in Bot's auth key.
    updater = Updater(token=pm.tokenbot, use_context=True)
    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(
        'start', start, run_async=True))

    # Message Handler harus d pasang paling terakhir
    dispatcher.add_handler(MessageHandler(Filters.text, read_command))
    # Start polling
    updater.start_polling()
    # Stop
    updater.idle()


if __name__ == '__main__':
    main()
