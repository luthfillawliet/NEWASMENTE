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
    print(update.message.chat_id)
    if (update.message.text[:2] == "ct" or update.message.text[:2] == "Ct" or update.message.text[:2] == "CT"):
        # Eksekusi buat CT
        context.bot.send_message(
            chat_id=pm.chat_id, text="Memulai pembuatan CT Idpel : \n"+update.message.text[3:15]+"\nKode Unit : "+update.message.text[16:21]+"\nKeterangan : "+update.message.text[22:])
        status, message = Asmente.buatCT(
            id_pelanggan=update.message.text[3:15], kodeunit=update.message.text[16:21], keteranganCT=update.message.text[22:])
        if (status == "yes"):
            print("STATUS MAIN : ", message)
            context.bot.send_message(chat_id=pm.chat_id, text=message)
            time.sleep(2)
            resp = requests.post(
                "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(pm.chat_id), files=fm.send_photos(pm.files_foto_ct))
        else:
            print("STATUS MAIN : ", message)
            context.bot.send_message(chat_id=pm.chat_id, text=message)
    elif ((update.message.text[:4] == "info" and update.message.text[4:5] == "|") or (update.message.text[:4] == "Info" and update.message.text[4:5] == "|") or (update.message.text[:4] == "INFO" and update.message.text[4:5] == "|")):
        if (update.message.text[5:6] == "0"):
            context.bot.send_message(
                chat_id=pm.chat_id, text="Memulai Pencarian Informasi Idpel : \n"+update.message.text[7:])
            [status, informasi, message] = Asmente.cek_infopelanggan(
                tipe_pencarian="Id Pelanggan", nomor_id=update.message.text[7:], link_infopelanggan=pm.link_info_pelanggan)
            context.bot.send_message(
                chat_id=pm.chat_id, text="Info Pelanggan berdasarkan Id Pelanggan :\n"+informasi)
        elif (update.message.text[5:6] == "1"):
            context.bot.send_message(
                chat_id=pm.chat_id, text="Memulai Pencarian Informasi Nomor Meter :\n"+update.message.text[7:])
            [status, informasi, message] = Asmente.cek_infopelanggan(
                tipe_pencarian="Nomor Meter", nomor_id=update.message.text[7:], link_infopelanggan=pm.link_info_pelanggan)
            context.bot.send_message(
                chat_id=pm.chat_id, text="Info Pelanggan berdasarkan Nomor Meter \n:"+informasi)
        else:
            context.bot.send_message(
                chat_id=pm.chat_id, text="Tipe Pencarian tidak ditemukan")
    elif (update.message.text[:8] == "infoacmt" and update.message.text[8:9] == "|" or update.message.text[:8] == "Infoacmt" and update.message.text[8:9] == "|" or update.message.text[:8] == "INFOACMT" and update.message.text[8:9] == "|"):
        context.bot.send_message(
            chat_id=pm.chat_id, text="Memulai pengecekan Info pelanggan ACMT idpel : "+update.message.text[9:])
        [status, informasi, message] = Asmente.info_pelanggan_acmt(
            id_pelanggan=update.message.text[9:])
        context.bot.send_message(
            chat_id=pm.chat_id, text=informasi)

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
