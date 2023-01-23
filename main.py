from ASMENTE import Asmente
from parameter import Parameter
from DataFrame import dataframe
from FILEMANAGER import filemanager
import time
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import requests
# Import Amicon object
from scraper import Amicon
from post_api import get_gardu
import logging

pm = Parameter()
fm = filemanager()
# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    chat_id = update.message.chat_id
    query = update.callback_query
    context.bot.send_message(
        chat_id=chat_id, text="Bot Standby...")


def findnth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)

# List perintah Asmen TE


def read_command(update, context):
    # chat_id = pm.chat_id
    chat_id = update.message.chat_id
    print(update.message.chat_id)
    [status, message] = Asmente.is_user_authenticated(chat_id=chat_id)
    if (status == "yes"):
        if (update.message.text[:2] == "ct" or update.message.text[:2] == "Ct" or update.message.text[:2] == "CT"):
            [status_kdunit, message_kdunit] = Asmente.kdunit_user(
                chat_id=chat_id, kode_unit=update.message.text[16:21])
            if (status_kdunit == "yes"):
                # Eksekusi buat CT
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai pembuatan CT Idpel : \n"+update.message.text[3:15]+"\nKode Unit : "+update.message.text[16:21]+"\nKeterangan : "+update.message.text[22:])
                status, message = Asmente.buatCT(
                    id_pelanggan=update.message.text[3:15], kodeunit=update.message.text[16:21], keteranganCT=update.message.text[22:])
                if (status == "yes"):
                    print("STATUS MAIN : ", message)
                    context.bot.send_message(chat_id=chat_id, text=message)
                    time.sleep(2)
                    resp = requests.post(
                        "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(chat_id), files=fm.send_photos(pm.files_foto_ct))
                    # Write log data
                    dat = dataframe()
                    dat.log_data(chat_id=chat_id,
                                 activity="clear tamper idpel :"+update.message.text[3:15], time=str(datetime.datetime.now()))
                else:
                    print("STATUS MAIN : ", message)
                    context.bot.send_message(chat_id=chat_id, text=message)
            elif (status_kdunit == "no"):
                context.bot.send_message(
                    chat_id=chat_id, text=message_kdunit)
        elif ((update.message.text[:4] == "info" and update.message.text[4:5] == "|") or (update.message.text[:4] == "Info" and update.message.text[4:5] == "|") or (update.message.text[:4] == "INFO" and update.message.text[4:5] == "|")):
            if (update.message.text[5:6] == "0"):
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai Pencarian Informasi Idpel : \n"+update.message.text[7:])
                [status, informasi, message] = Asmente.cek_infopelanggan(
                    tipe_pencarian="Id Pelanggan", nomor_id=update.message.text[7:], link_infopelanggan=pm.link_info_pelanggan)
                context.bot.send_message(
                    chat_id=chat_id, text="Info Pelanggan berdasarkan Id Pelanggan :\n"+informasi)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                             activity="Info Pelanggan", time=str(datetime.datetime.now()))
            elif (update.message.text[5:6] == "1"):
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai Pencarian Informasi Nomor Meter :\n"+update.message.text[7:])
                [status, informasi, message] = Asmente.cek_infopelanggan(
                    tipe_pencarian="Nomor Meter", nomor_id=update.message.text[7:], link_infopelanggan=pm.link_info_pelanggan)
                context.bot.send_message(
                    chat_id=chat_id, text="Info Pelanggan berdasarkan Nomor Meter \n:"+informasi)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                             activity="Info Pelanggan", time=str(datetime.datetime.now()))
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Tipe Pencarian tidak ditemukan")
        elif (update.message.text[:8] == "infoacmt" and update.message.text[8:9] == "|" or update.message.text[:8] == "Infoacmt" and update.message.text[8:9] == "|" or update.message.text[:8] == "INFOACMT" and update.message.text[8:9] == "|"):
            context.bot.send_message(
                chat_id=chat_id, text="Memulai pengecekan Info pelanggan ACMT idpel : "+update.message.text[9:])
            [status, informasi, message] = Asmente.info_pelanggan_acmt(
                id_pelanggan=update.message.text[9:])
            context.bot.send_message(
                chat_id=chat_id, text=informasi)
            context.bot.send_message(
                chat_id=chat_id, text=message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                         activity="Info ACMT", time=str(datetime.datetime.now()))
        elif (update.message.text[:9] == "resetimei" or update.message.text[:9] == "Resetimei" or update.message.text[:9] == "RESETIMEI"):
            id_input = update.message.text[16:]
            kode_unit = update.message.text[10:15]
            context.bot.send_message(
                chat_id=chat_id, text="Memulai reset imei petugas id : "+kode_unit+"."+id_input)
            [status, message] = Asmente.reset_imei(
                kode_unit=kode_unit, user_id=id_input)
            if (status == "yes"):
                context.bot.send_message(
                    chat_id=chat_id, text=message)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                             activity="reset imei", time=str(datetime.datetime.now()))
            else:
                context.bot.send_message(
                    chat_id=chat_id, text=message)
        elif (update.message.text[:9] == "Aktifasi" or update.message.text[:9] == "aktifasi" or update.message.text[:9] == "AKTIFASI" or update.message.text[:9] == "Aktivasi" or update.message.text[:9] == "aktivasi"):
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "admin" or level_user == "owner")):
                id_pelanggan = update.message.text[16:28]
                kode_unit = update.message.text[10:15]
                petugas_dan_keterangan = update.message.text[29:]
                print("Memulai aktivasi meter")
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai aktivasi meter idpel : "+id_pelanggan+"\n"+"Kode Unit : "+kode_unit+"\nKeterangan : "+petugas_dan_keterangan)
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Periksa kembali command dan hak akses user")
        elif (update.message.text[:3] == "add" or update.message.text[:3] == "Add" or update.message.text[:3] == "ADD"):
            # cek level user
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "owner" or level_user == "admin")):
                separator_1 = findnth(update.message.text, "|", 1)
                separator_2 = findnth(update.message.text, "|", 2)
                separator_3 = findnth(update.message.text, "|", 3)
                separator_4 = findnth(update.message.text, "|", 4)
                chat_id_daftar = int(update.message.text[4:separator_1])
                nama = update.message.text[separator_2+1:separator_3]
                nomor_telfon = update.message.text[separator_3+1:separator_4]
                context.bot.send_message(
                    chat_id=pm.chat_id_admin, text="Memulai add user dengan chat id : "+str(chat_id_daftar)+"\n"+"Kode Unit : "+str(update.message.text[separator_1+1:separator_2]))
                [status, message] = Asmente.add_new_user(
                    chat_id_daftar=chat_id_daftar, kode_unit=update.message.text[separator_1+1:separator_2], nama=nama, nomor_telfon=nomor_telfon, level=update.message.text[separator_4+1:])
                context.bot.send_message(
                    chat_id=pm.chat_id_admin, text=message)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                             activity="Add user", time=str(datetime.datetime.now()))
            else:
                context.bot.send_message(
                    chat_id=update.message.chat_id, text="User tidak punya hak akses")
        elif (len(update.message.text) == 20 and (update.message.text[:7] == "Infokct" or update.message.text[:7] == "infokct")):
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Memulai cek info KCT KRN Idpel : "+update.message.text[8:])
            [status, message] = Asmente.get_kct_krn(
                Id_pelanggan=update.message.text[8:])
            context.bot.send_message(
                chat_id=update.message.chat_id, text=message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                         activity="Infokct krn", time=str(datetime.datetime.now()))
        elif (update.message.text[:10] == "Infoblokir" or update.message.text[:10] == "infoblokir"):
            context.bot.send_message(
                chat_id=chat_id, text="Memulai pengecekan blocking token idppel : "+update.message.text[11:])
            status, message = Asmente.cek_blocking_token(
                id_pelanggan=update.message.text[11:])
            context.bot.send_message(
                chat_id=chat_id, text=message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                         activity="Infoblokir", time=str(datetime.datetime.now()))
        else:
            print("command tidak dikenal")
            context.bot.send_message(
                chat_id=chat_id, text="command tidak dikenal")
    else:
        print(message)
        # notif ke user
        context.bot.send_message(
            chat_id=chat_id, text=message)
        # notif ke admin
        context.bot.send_message(
            chat_id=pm.chat_id_admin, text="Chatid tidak dikenal mencoba masuk")
        context.bot.send_message(
            chat_id=pm.chat_id_admin, text=str(chat_id))


def log_info(update: Update):
    chat_id = update.message.chat_id
    user = update.effective_user.full_name
    waktu = datetime.datetime.now()

    print(f'{waktu} - group: {chat_id} - user: {user}')


def start_sigadis(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=f'Hai {update.effective_user.first_name} Selamat datang, silahkan ketik /update ',
        parse_mode='markdown'
    )


def update_data(update: Update, context: CallbackContext):
    log_info(update)
    update.message.reply_text(
        text='Baik, mohon tunggu...', parse_mode='markdown')
    try:
        s = time.perf_counter()
        bot = Amicon(username=pm.username_amicon, password=pm.password_amicon)
        result = bot.download_data(get_gardu())
        f = time.perf_counter()
        waktu = round((f - s), 2)
        update.message.reply_text(
            text=f'Berhasil update data Gardu dari AMICON ({waktu}s)'
                 f'\nBerhasil : {result["berhasil"]}\n'
                 f'Gagal : {result["gagal"]}\n',
            parse_mode='markdown')
    except Exception as e:
        update.message.reply_text(
            text='Gagal Update data Gardu dari AMICON',
            parse_mode='markdown')
        return


def update_data_otomatis(context: CallbackContext):
    """Fungsi ini membuat Thread untuk update masing2 UP3"""
    try:
        s = time.perf_counter()
        bot = Amicon(username=pm.username_amicon, password=pm.password_amicon)
        bot.download_data(get_gardu())
        f = time.perf_counter()
        waktu = round((f - s), 2)
        context.bot.send_message(text=f'Berhasil update data Gardu dari AMICON ({waktu}s)',
                                 reply_markup='markdown')
    except Exception as e:
        context.bot.send_message(
            text='Gagal Update data Gardu dari AMICON',
            parse_mode='markdown')
        return


def main():
    # bot Telegram
    # Create updater and pass in Bot's auth key.
    updater = Updater(token=pm.tokenbot, use_context=True)
    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Mengecek kesiapan bot
    dispatcher.add_handler(CommandHandler(
        'start', start, run_async=True))
    # Run Aplikasi si gadis
    dispatcher.add_handler(CommandHandler('start_sigadis', update_data))

    # Run daily basis
    # Membuat scheduler untuk update saldo tunggakan
    j = updater.job_queue
    # Jam 3.30 setiap hari
    j.run_daily(
        update_data_otomatis,
        days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=10, minute=39, second=00)
    )

    # Message Handler harus d pasang paling terakhir
    dispatcher.add_handler(MessageHandler(Filters.text, read_command))
    # Start polling
    updater.start_polling()
    # Stop
    updater.idle()


if __name__ == '__main__':
    main()
