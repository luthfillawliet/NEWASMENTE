from ASMENTE import Asmente
from ASMENTE import ReplyButton
from AMICONBOT import AmiconBot
from parameter import Parameter
from DataFrame import dataframe
from FILEMANAGER import filemanager
import time
import datetime
import telegram
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import requests
# Import Amicon object
from scraper import Amicon
from scraper import AP2T


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
    [status, message] = Asmente.is_user_authenticated(chat_id=chat_id)
    if (status == "yes"):
        context.bot.send_message(
            chat_id=chat_id, text="Bot Standby...")
    else:
        context.bot.send_message(
            chat_id=chat_id, text=message)
        # notif ke admin
        context.bot.send_message(
            chat_id=pm.chat_id_admin, text="Chatid tidak dikenal mencoba masuk")
        context.bot.send_message(
            chat_id=pm.chat_id_admin, text=str(chat_id))

def start_amicon(update,context):
    chat_id = update.message.chat_id
    reply_markup = AmiconBot.start()
    context.bot.send_message(
            chat_id=chat_id, text="Silahkan pilih salah satu", reply_markup=reply_markup)

def informasi(update, context):
    chat_id = update.message.chat_id
    [status, message] = Asmente.is_user_authenticated(chat_id=chat_id)
    if (status == "yes"):
        text1 = "1. Untuk mengakses info pelanggan dengan idpel, silahkan ketik :\n'Info|0|12 digit idpel , contoh Info|0|32131xxxxxxx'\nPencarian denga nomor meter 'Info|1|nomor meter' , contoh Info|1|450xxxxxxxx\n"
        text2 = "2. Untuk mengakses info pelanggan via ACMT dengan idpel. silahkan ketik 'Infoacmt|12 digit idpel' , contoh : Infoacmt 32111xxxxxxx\n"
        text3 = "3. Untuk mengakses Info blocking token dari AP2T dengan idpel, silahkan ketik : Infoblokir|12 digit Idpel , contoh : Infoblokir|32121xxxxxxx\n"
        text4 = "4. Untuk mengakses token KCT Upgrade KRN dengan idpel, silahkan ketik : Infokct idpel, contoh : Infokct 32131xxxxxxx\n"
        text5 = "5. Untuk pembbuatan CT, ketik 'Ct|12 Digit Idpel|kode unit|Keterangan (Penyebab periksa, petugas dan keterangan lainnya)'\ncontoh : Ct|32131xxxxxxx|32131|ganti mcb, petugas fulan\n"
        text6 = "6. Untuk menambah user baru (Hanya bisa di akses untuk role admin), ketik 'Add|chat_id|kode unit|Nama User|Nomor Telfon|level user'\nContoh : 'Add|817654873|32131|Fulan bin fulan|081321765487|user\n"
        text7 = "7. Untuk reset Imei HP ACMT petugas Cater, ketik 'Resetimei|Kode unit|user petugas (tanpa kode uni)' , Contoh : Resetimei|32131|sitaba\n"
        text8 = "8. Untuk Cek monitoring permohonan token berdasarkan Idpelnomor meter (kode 0 untuk idpel, 1 untuk nomor emter), 'ketik Montok|kode pencarian (0 / 1)|id pelanggan/nomor meter (sesuai dengan kategori)', contoh Montok|0|321500xxxxxx , atau Montok|1|14456787659\n"
        text9 = "9. Untuk cetak KCT dari Nomor Agenda, bisa ketik 'Cetakkct|18 digit Nomor Agenda' ,contoh : Cetakkct|321310054567857456\n"
        text10 = "10. Untuk cek History pembelian token Prabayar, ketik 'Infotoken|12 digit Idpel', contoh : Infotoken|321114598716"
        text11 = "11. Untuk cek Foto 1 (Stand), foto 2, dan foto rumah di ACMT, ketik 'fotoacmt|12 digit idpel', contoh : fotoacmt|321114598716"
        text_penutup = "Info lebih lanjut silahkan hubungi Luthfil, TL DALSUT UP3 Makassar selatan"
        merge_text = text1+text2+text3+text4+text5+text6+text7+text8+text9+text10+text11+text_penutup
        context.bot.send_message(
            chat_id=chat_id, text="Informasi cara pemakaian : "+"\n"+merge_text)
    else:
        context.bot.send_message(
            chat_id=chat_id, text=message)
        # notif ke admin
        context.bot.send_message(
            chat_id=pm.chat_id_admin, text="Chatid tidak dikenal mencoba masuk")
        context.bot.send_message(
            chat_id=pm.chat_id_admin, text=str(chat_id))

def updateuser(update,context):
    chat_id = update.message.chat_id
    [status, message] = Asmente.is_user_authenticated(chat_id=chat_id)
    if (status == "yes"):
        #cek level autentikasi User
        [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
        if (status == "yes" and (level_user == "owner" or level_user == "admin")):
            context.bot.send_message(
                chat_id=chat_id, text="update|NIP(Angka dan Huruf Kapital|kode yang akan di update\n"+
                    "List Kode :\n"+
                    "1 : Kode unit\n2 : Nama\n3 : Jabatan\n4 : Password AP2T\nContoh jika akan mengupdate Password\n"+
                    "update|1234567ZY|4")
            context.bot.send_message(
                chat_id=chat_id, text="update|94171287ZY|4")
        else:
            context.bot.send_message(
                chat_id=chat_id, text="Mengupdate user hanya untuk role Owner dan Admin, silahkan kontak Luthfil")
    else:
        context.bot.send_message(
            chat_id=chat_id, text=message)
        # notif ke admin
        context.bot.send_message(
            chat_id=pm.chat_id_admin, text="Chatid tidak dikenal mencoba masuk")
        context.bot.send_message(
            chat_id=pm.chat_id_admin, text=str(chat_id))
        
def findnth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)
def get_result(value):
    result_dict = {
        "1": 'kodeunit',
        "2": 'nama',
        "3": 'jabatan',
        "4": 'password',
    }
    return result_dict.get(value, 'Invalid value')
# List perintah Asmen TE


def button(update, context):
    query = update.callback_query
    context.bot.send_message(text="Yang dipilih : %s" %
                             query.data, chat_id=query.message.chat_id)
    message = ReplyButton.execute_button(
        data=query.data, kode_unit="32131")
    # Coba kirim respon
    context.bot.send_message(
        chat_id=query.message.chat_id, text=message)


def read_command(update, context):
    # chat_id = pm.chat_id
    chat_id = update.message.chat_id
    print(update.message.chat_id)
    [status, message] = Asmente.is_user_authenticated(chat_id=chat_id)
    if (status == "yes"):
        # COmmand untuk semua user yang terautentikasi
        if (update.message.text[:2] == "ct" or update.message.text[:2] == "Ct" or update.message.text[:2] == "CT"):
            [status_kdunit, message_kdunit] = Asmente.kdunit_user(
                chat_id=chat_id, kode_unit=update.message.text[16:21])
            if (status_kdunit == "yes"):
                # Eksekusi buat CT
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai pembuatan CT Idpel : \n"+update.message.text[3:15]+"\nKode Unit : "+update.message.text[16:21]+"\nKeterangan : "+update.message.text[22:])
                status, jumlahct, message = Asmente.buatCT(
                    id_pelanggan=update.message.text[3:15], kodeunit=update.message.text[16:21], keteranganCT=update.message.text[22:])
                if (status == "yes"):
                    print("STATUS MAIN : ", message)
                    # Kirim jumlah permintaan CT
                    context.bot.send_message(
                        chat_id=chat_id, text="Jumlah Permintaan CT : "+str(jumlahct))
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
        elif ((update.message.text[:6] == "montok" or update.message.text[:6] == "Montok" or update.message.text[:6] == "MONTOK") and len(update.message.text) > 18):
            # cek tipe pencarian
            tipe_pencarian = update.message.text[7:8]
            id_pencarian = update.message.text[9:]
            if (tipe_pencarian == "0"):
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai monitoring permohonan token Idpel : "+id_pencarian)
                status, message = Asmente.info_montok(
                    url_montok=pm.link_montok, tipe_pencarian=tipe_pencarian, id_pencarian=id_pencarian)
                if (status == "yes"):
                    context.bot.send_message(
                        chat_id=chat_id, text="Hasil monitoring permohonan token Id pelanggan : "+id_pencarian+"\n"+message)
                else:
                    context.bot.send_message(
                        chat_id=chat_id, text="Gagal monitoring permohonan token Id pelanggan : "+id_pencarian+"\n"+message)
            elif (tipe_pencarian == "1"):
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai monitoring permohonan token Nomor Meter : "+id_pencarian)
                status, message = Asmente.info_montok(
                    url_montok=pm.link_montok, tipe_pencarian=tipe_pencarian, id_pencarian=id_pencarian)
                if (status == "yes"):
                    context.bot.send_message(
                        chat_id=chat_id, text="Hasil monitoring permohonan token Nomor meter : "+id_pencarian+"\n"+message)
                else:
                    context.bot.send_message(
                        chat_id=chat_id, text="Gagal monitoring permohonan token Nomor Meter : "+id_pencarian+"\n"+message)
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Tipe Pencarian tidak diketahui")
        elif ((update.message.text[:8] == "Aktifasi" or update.message.text[:8] == "aktifasi" or update.message.text[:8] == "AKTIFASI" or update.message.text[:8] == "Aktivasi" or update.message.text[:8] == "aktivasi") and len(update.message.text) == 8):
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "admin" or level_user == "owner")):
                # kode_unit = update.message.text[10:15]
                # id_pelanggan = update.message.text[16:28]
                # petugas_dan_keterangan = update.message.text[29:]
                print("Memulai buat pengaduan meter")
                reply_markup = ReplyButton.opsi_aktivasi()
                query = update.callback_query
                update.message.reply_text(
                    'SIlahkan pilih :', reply_markup=reply_markup)
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
                    chat_id_daftar=chat_id_daftar, kode_unit=int(update.message.text[separator_1+1:separator_2]), nama=nama, nomor_telfon=nomor_telfon, level=update.message.text[separator_4+1:])
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
        #cek pembelian token
        elif (update.message.text[:10] == "infotoken|" or update.message.text[:10] == "Infotoken|" or update.message.text[:10] == "INFOTOKEN|"):
            #cek digit idpel
            id_pelanggan = update.message.text[10:]
            if(len(id_pelanggan) == 12):
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai pencarian history pembelian token Idpel "+id_pelanggan+" : ")
                [status,informasi,message] = Asmente.cek_pembelian_token(id_pelanggan)
                if(status=="yes"):
                    context.bot.send_message(
                        chat_id=chat_id, text=informasi)
                else:
                    context.bot.send_message(
                        chat_id=chat_id, text=message)
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Periksa idpel dengan benar")
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                            activity="Info Pembelian token", time=str(datetime.datetime.now()))
        elif ((update.message.text[:8] == "cetakkct" or update.message.text[:8] == "Cetakkct" or update.message.text[:8] == "CETAKKCT") and len(update.message.text) > 25):
            context.bot.send_message(
                chat_id=chat_id, text="Memulai cetak KCT Token dengan nomor agenda : "+update.message.text[9:])
            ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver, filepathenkripsi=pm.filepathenkripsi,
                        urlap2t=pm.urlap2t, download_dir=pm.download_dir, filepathct=pm.filepathct, user_options=pm.user_options)
            status, message = ap2t.cetak_token(
                nomoragenda=update.message.text[9:], link_ct=pm.baselink_kct)
            if (status == "yes"):
                status, message = ap2t.take_screenshoot(
                    direktori=pm.filepathct, file_name="foto_kct.png", index=pm.index, numbertab=1)
                if (status == "yes"):
                    resp = requests.post(
                        "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(chat_id), files=fm.send_photos(pm.files_foto_ct))
                else:
                    context.bot.send_message(
                        chat_id=chat_id, text="Gagal kirim screenshoot token\nError Meesage : "+message)
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Gagal cetak token\nError Meesage : "+message)
        #Fungsi Manajemen User
        elif ((update.message.text[:9] == "broadcast" or update.message.text[:9] == "Broadcast") and update.message.text[9:10] == "|"):
            # cek level user
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "owner" or level_user == "admin")):
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai mengirim pesan broadcast")
                df = dataframe.get_all_userid(pm.filepathlistuser, "all")
                pesan = update.message.text[(findnth(
                    update.message.text, "|", 1)+1):]
                for i in df:
                    # print("chat id : ", str(i))
                    try:
                        context.bot.send_message(
                            chat_id=i, text="Pesan Broadcast dari Admin : ")
                        context.bot.send_message(
                            chat_id=i, text=pesan+"\n\n"+update.message.text[findnth(update.message.text, "|", 0)+1:findnth(update.message.text, "|", 1)])
                        # Write log data
                        dat = dataframe()
                        dat.log_data(chat_id=chat_id,
                                     activity="Broadcast by : "+chat_id, time=str(datetime.datetime.now()))
                    except:
                        pass
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Level user tidak memiliki autentikasi")
        elif((update.message.text[:7] == "update|" or update.message.text[:7] == "Update|" or update.message.text[:7] == "UPDATE|") and len(update.message.text) > 10):
            #cek level autentikasi User
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "owner" or level_user == "admin")):
                separator_2 = findnth(update.message.text, "|", 2)
                update_value = update.message.text[(separator_2+1):]
                item_update = get_result(update.message.text[separator_2-1])
                print(update.message.text[separator_2-1])
                context.bot.send_message(
                    chat_id=chat_id, text="Memulai Update "+item_update+" User NIP "+update.message.text[7:separator_2-2])
                column_objective = "B"
                if(item_update == "password"):
                    column_objective = "E"
                else:
                    column_objective = "B"
                daf = dataframe()
                daf.update_user_data(filepathlistuser=pm.filepathlistuser,sheetname="Sheet1",column_lookup="NIP",input_value="1234567ZY",updated_value=update_value,column_objective=column_objective)
                
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Mengupdate user hanya untuk role Owner dan Admin, silahkan kontak Luthfil")
        # fungsi aktivasi meter
        elif ((update.message.text[:9] == "pengaduan" or update.message.text[:9] == "Pengaduan" or update.message.text[:9] == "PENGADUAN") and update.message.text[9:10] == "|"):
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "owner" or level_user == "admin")):
                # Get kode unitnya dulu
                kodeunit = update.message.text[10:15]
                print("Kode unit chat id : ", kodeunit)
                status, kodeunitbanding, message = Asmente.get_kode_unit(
                    chat_id=chat_id)
                print("Kode unit bandig dr excel : ", kodeunitbanding)
                if (status == "yes" and kodeunit == str(kodeunitbanding)):
                    id_pelanggan = update.message.text[16:28]
                    nomor_meter_lama = update.message.text[29:40]
                    keterangan = update.message.text[41:]
                    context.bot.send_message(
                        chat_id=chat_id, text="Memulai Aktivasi kWh Meter\nIdpel : "+id_pelanggan+"\nKode Unit : "+update.message.text[10:15]+"\nNomor Meter Lama : "+nomor_meter_lama+"\nKeterangan : "+keterangan)
                    [status, message, nomoragenda] = Asmente.buatPengaduanHarAPP(
                        id_pelanggan=id_pelanggan, kode_unit=kodeunit, nomor_meter_lama=nomor_meter_lama, keterangan=keterangan)
                    if (status == "yes" and nomoragenda != 0):
                        context.bot.send_message(
                            chat_id=chat_id, text="tindakan|"+kodeunit+"|"+str(nomoragenda))
                    else:
                        context.bot.send_message(
                            chat_id=chat_id, text="Gagal buat pengaduan\nMessage Error : "+message)
                    # Write log data
                    dat = dataframe()
                    dat.log_data(chat_id=chat_id,
                                 activity="Buat pengaduan APP Idpel : "+id_pelanggan, time=str(datetime.datetime.now()))
                else:
                    context.bot.send_message(
                        chat_id=chat_id, text="Kode Unit user tidak sesuai")
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="User tidak punya hak akses")
        elif ((update.message.text[:8] == "tindakan" or update.message.text[:8] == "Tindakan" or update.message.text[:8] == "TINDAKAN") and len(update.message.text) == 33):
            kode_unit = update.message.text[9:14]
            nomoragenda = update.message.text[15:]
            context.bot.send_message(
                chat_id=chat_id, text="Memulai save tindakan pengaduan\nNomor Agenda : "+nomoragenda+"\nKode Unit : "+kode_unit)
            status, message, nomoragenda = Asmente.tindakanPengaduanHarAPP(
                nomoragenda=int(nomoragenda), kode_unit=kode_unit)
            if (status == "yes"):
                context.bot.send_message(
                    chat_id=chat_id, text="Berhasil save tindakan pengaduan Nomor Agenda " +
                    str(nomoragenda))
                context.bot.send_message(
                    chat_id=chat_id, text="aktivasiapp|"+kode_unit+"|"+str(nomoragenda)+"|"+"Nomor Meter Baru")
            else:
                context.bot.send_message(
                    chat_id=chat_id, text=message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                         activity="Save tindakan pengaduan Agenda: "+str(nomoragenda), time=str(datetime.datetime.now()))
        elif ((update.message.text[:11] == "aktivasiapp" or update.message.text[:11] == "Aktivasiapp" or update.message.text[:11] == "AKTIVASIAPP") and len(update.message.text) == 48):
            kode_unit = update.message.text[12:17]
            nomoragenda = update.message.text[18:36]
            nomor_meter_baru = update.message.text[37:]
            context.bot.send_message(
                chat_id=chat_id, text="Memulai aktivasi kWh meter dengan nomor agenda : "+nomoragenda+"\nNomor meter baru : "+nomor_meter_baru+"\nKode Unit : "+kode_unit)
            status, message, nomoragenda = Asmente.aktivasiHarAPP(nomoragenda=int(
                nomoragenda), kode_unit=kode_unit, nomor_meter_baru=nomor_meter_baru)
            if (status == "yes" and nomoragenda != 0):
                context.bot.send_message(
                    chat_id=chat_id, text="cetakkct|"+str(nomoragenda))
            else:
                context.bot.send_message(
                    chat_id=chat_id, text=message)
        elif ((update.message.text[:10] == "tagsusp2tl" or update.message.text[:10] == "Tagsusp2tl" or update.message.text[:10] == "TAGSUSP2TL")):
            #cek level autentikasi User
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "owner" or level_user == "admin")):
                context.bot.send_message(
                        chat_id=chat_id, text="Memulai Pembuatan Laporan Tagihan Susulan Hari ini")
                df = dataframe()
                tahun_bulan = dataframe.get_tahun_bulan_sekarang() #jangan lupa jadikan variabel
                [status,kode_unit_user,message] = df.get_kode_unit_user_tagsus(chat_id=chat_id)
                if(status == "yes"):
                    [status,message] = Asmente.create_lap_tsp2tl(kode_unit_user = kode_unit_user,tahun_bulan = tahun_bulan)
                    context.bot.send_message(
                        chat_id=chat_id, text=message)
                    if(status == "yes"):
                        #kirim file ke chat
                        try:
                            document = open("data//downloads//ReportServlet.xls","rb")
                            context.bot.send_document(chat_id,document)
                            message = "Berhasil kirim File"
                            print(message)
                            context.bot.send_message(
                                chat_id=chat_id, text=message)
                        except Exception as e:
                            message = "Gagal kirim file\nMessage Error : \n"+str(e)
                            context.bot.send_message(
                                chat_id=chat_id, text="Gagal kirim file\n"+message)
                    else:
                        context.bot.send_message(
                            chat_id=chat_id, text="Gagal kirim file\n"+message)
                else:
                    context.bot.send_message(
                        chat_id=chat_id, text="Gagal ambil kode unit\n"+message)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                                activity="Update Laporan TS Harian", time=str(datetime.datetime.now()))
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Update Laporan Harian hanya untuk level Admin atau Owner")
        elif((update.message.text[:8] == "fotoacmt" or update.message.text[:8] == "Fotoacmt" or update.message.text[:8] == "FOTOACMT") and len(update.message.text) == 21):
            idpel = update.message.text[9:]
            context.bot.send_message(
                chat_id=chat_id, text="Memulai kirim foto ACMT Idpel "+idpel)
            status1,status2,statusrumah = Asmente.get_foto_rumah(idpelanggan=idpel)
            if(statusrumah == "yes"):
                resp = requests.post(
                            "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(chat_id), files=fm.send_photos(pm.files_foto_rumah))
                context.bot.send_message(
                    chat_id=chat_id, text="Foto Rumah Berhasil di kirim")
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Gagal get foto rumah")
            if(status1 == "yes"):
                resp = requests.post(
                            "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(chat_id), files=fm.send_photos(pm.files_foto_1))
                context.bot.send_message(
                    chat_id=chat_id, text="Foto 1 Berhasil di kirim")
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Gagal kirim foto 1")
            if(status2 == "yes"):
                resp = requests.post(
                            "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(chat_id), files=fm.send_photos(pm.files_foto_2))
                context.bot.send_message(
                    chat_id=chat_id, text="Foto 2 Berhasil di kirim")
            else:
                context.bot.send_message(
                    chat_id=chat_id, text="Gagal kirim foto rumah")
            
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                            activity="Foto ACMT idpel : "+idpel, time=str(datetime.datetime.now()))          
        elif((update.message.text[:10] == "kirimlapts" or update.message.text[:10] == "Kirimlapts" or update.message.text[:10] == "KIRIMLAPTS")):
            context.bot.send_message(
                chat_id=chat_id, text="Memulai kirim laporan TS Hari ini")
            [status,message] = Asmente.kirim_report_ts()
            if(status == "yes"):
                print(message)
                context.bot.send_message(
                    chat_id=chat_id, text="Berhasil mengupdate Laporan TS P2TL pada spreadsheet")
                try:
                    document = open("fotoct//screenshot_ts.png","rb")
                    context.bot.send_document(chat_id,document)
                    message = "Berhasil kirim Foto"
                    print(message)
                    context.bot.send_message(
                        chat_id=chat_id, text=message)
                except Exception as e:
                    message = "Gagal kirim foto\nMessage Error : \n"+str(e)
                    print(message)
                    context.bot.send_message(
                        chat_id=chat_id, text=message)
            else:
                context.bot.send_message(
                    chat_id=chat_id, text=message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                            activity="Kirim Laporan TS Harian", time=str(datetime.datetime.now()))
        
        #Fungsi Bot AMICON Register Asset dan Comissioning
        #Asset
        elif((update.message.text[:] == "ASSET")):
            message = update.message.text[:]
            bot = AmiconBot()
            bot.get_first_choice(message=message)
            context.bot.send_message(
                chat_id=chat_id, text="Silahkan Pilih Tipe Aset : ", reply_markup=bot.set_asset_choice())
        elif((update.message.text[:] == "METER")):
            message = update.message.text[:]
            bot = AmiconBot()
            bot.get_selected_asset(selected_aset=message)
            context.bot.send_message(
                chat_id=chat_id, text="Silahkan Pilih Tipe Merk : ", reply_markup=bot.set_meter_brand())
        elif(update.message.text[:] == "EDMI"):
            message = update.message.text[:]
            bot = AmiconBot()
            bot.get_selected_brand(selected_brand=message)
            context.bot.send_message(
                chat_id=chat_id, text="Silahkan Pilih Tipe Merk : ", reply_markup=bot.set_brand_type(selected_brand=message))
        elif(update.message.text[:] == "ITRON"):
            message = update.message.text[:]
            bot = AmiconBot()
            bot.get_selected_brand(selected_brand=message)
            context.bot.send_message(
                chat_id=chat_id, text="Silahkan Pilih Tipe Merk : ", reply_markup=bot.set_brand_type(selected_brand=message))
        #Comissioning
        elif(update.message.text[:] == "COMMISSIONING"):
            message = "COMMISSIONING|32XXXXXXXXXX"
            context.bot.send_message(
                chat_id=chat_id, text=message)
        elif(update.message.text[:13] == "COMMISSIONING" and len(update.message.text)== 26):
            idpel = update.message.text[14:]
            context.bot.send_message(
                chat_id=chat_id, text="Memulai Comissioning Pelanggan ID : "+idpel)
            amicon = Amicon(username=pm.username_amicon,password=pm.password_amicon)
            amicon.first_page()
            status_login,message = amicon.cek_login()
            result = ""
            if(status_login == "no"):
                print(message)
                result,message = Asmente.execute_amicon_not_login_state(idpel=idpel,amicon=amicon)     
            else:
                print(message)
                result,message = Asmente.execute_amicon_login_state(idpel=idpel,amicon=amicon)
            #Menunggu proses download
            time.sleep(10)
            if(result == "success"):
                context.bot.send_message(
                chat_id=chat_id, text="Berhasil melakukan Comissioning Idpel : "+idpel)
                path = "data//downloads"
                status,most_recent_files = filemanager.select_last_modified_files(path=path)
                try:
                    document = open(path+"//"+most_recent_files,"rb")
                    context.bot.send_document(chat_id,document)
                    message = "Berhasil kirim File"
                    print(message)
                    context.bot.send_message(
                        chat_id=chat_id, text=message)
                except Exception as e:
                    message = "Gagal kirim file\nMessage Error : \n"+str(e)
                    context.bot.send_message(
                        chat_id=chat_id, text="Gagal kirim file\n"+message)
            else:
                context.bot.send_message(
                        chat_id=chat_id, text="Gagal Comissioning"+message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                            activity="Comissioning : "+idpel, time=str(datetime.datetime.now()))
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
        bot = Amicon(username=pm.username_amicon,
                     password=pm.password_amicon)
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
        bot = Amicon(username=pm.username_amicon,
                     password=pm.password_amicon)
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
    # Mengecek kesiapan bot
    dispatcher.add_handler(CommandHandler(
        'informasi', informasi, run_async=True))
    # Mengecek kesiapan bot
    dispatcher.add_handler(CommandHandler(
        'updateuser', updateuser, run_async=True))
    # Run Aplikasi si gadis
    dispatcher.add_handler(CommandHandler('start_sigadis', start_sigadis))
    dispatcher.add_handler(CommandHandler('update', update_data))
    # Run Aplikasi si Amicon
    dispatcher.add_handler(CommandHandler('start_amicon', start_amicon))
    # Run daily basis
    # Membuat scheduler untuk update saldo tunggakan
    j = updater.job_queue
    # Jam 3.30 setiap hari
    # j.run_daily(
    #     update_data_otomatis,
    #     days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=10, minute=39, second=00)
    # )
    # Message Handler harus d pasang paling terakhir
    dispatcher.add_handler(MessageHandler(Filters.text, read_command))
    dispatcher.add_handler(CallbackQueryHandler(button))
    # Start polling
    updater.start_polling()
    # Stop
    updater.idle()


if __name__ == '__main__':
    main()
