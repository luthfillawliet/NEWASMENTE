from ASMENTE import Asmente
from ASMENTE import ReplyButton
from AMICONBOT import AmiconBot
from parameter import Parameter
from DataFrame import dataframe
from FILEMANAGER import filemanager
import time
import datetime
from datetime import time
import telegram
from telegram import Bot
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, JobQueue, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update # type: ignore
from telegram.ext import CallbackContext, Application # type: ignore
import requests
import updatelaporan
# Import Amicon object
from scraper import Amicon
from scraper import AP2T
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from pytz import timezone
import asyncio
import schedule
import locale


from post_api import get_gardu
import logging

pm = Parameter()
fm = filemanager()
df = dataframe()
# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the bot
bot = Bot(token=pm.tokenbot)


async def start(update, context):
    chat_id = update.message.chat_id
    query = update.callback_query
    [status, message] = Asmente.is_user_authenticated(chat_id=chat_id)
    if (status == "yes"):
        await context.bot.send_message(
            chat_id=chat_id, text="Bot Standby...")
        # start_menu(update, context)
    else:
        await context.bot.send_message(
            chat_id=chat_id, text=message)
        # notif ke admin
        await context.bot.send_message(
            chat_id=pm.chat_id_admin, text="Chatid tidak dikenal mencoba masuk")
        await context.bot.send_message(
            chat_id=pm.chat_id_admin, text=str(chat_id))
        
#Scheduled ask predefinition

desired_time = datetime.time(hour=9,minute=26,second=00)  #ATUR WAKTU YANG DI SCHEDULE KAN
waktuupdatep2tl = datetime.time(hour=10,minute=00,second=00) #Waktu update realisasi P2TL
waktulaporanjnmax = datetime.time(hour=11,minute=00,second=00) #Waktu kirim chat laporan JN max
waktuupdatespreadsheetuid = datetime.time(hour=12,minute=00,second=00)
waktuupdatekemarin = datetime.time(hour=12,minute=30,second=00) #Waktu update realisasi TS kemarin yang dilaporkan

async def your_job_function(context:CallbackContext):
    current_time = datetime.datetime.now()
    # Format the time string (optional)
    formatted_time = current_time.strftime("%H:%M:%S")  # Example: 20:11:13 (hour:minute:second)
    print(formatted_time)
    #Mengirim notif bahwa proses update data laporan akan dimulai
    await context.bot.send_message(
        chat_id=pm.chat_id_admin, text=f"Memulai mengirim laporan TS dan JN max pada pukul : {formatted_time}")
    
    # 1. Update data TS P2TL Terlebih dahulu
    await context.bot.send_message(chat_id=pm.chat_id_admin, text="Memulai Pembuatan Laporan Tagihan Susulan Hari ini")
    tahun_bulan = dataframe.get_tahun_bulan_sekarang() #jangan lupa jadikan variabel
    [status,kode_unit_user,message] = df.get_kode_unit_user_tagsus(chat_id=pm.chat_id_admin)
    if(status == "yes"):
    #  Ulang sebanyak 3 kali
        i = 0 #Set jumlah perulangan
        while i < 3:
            print ("Percobaan ke -"+str(i))
            await context.bot.send_message(
                chat_id=pm.chat_id_admin, text=f"memulai percobaan laporan ke {i+1}")
            try:
                [status,message] = Asmente.create_lap_tsp2tl(kode_unit_user = kode_unit_user,tahun_bulan = tahun_bulan)
                await context.bot.send_message(
                    chat_id=pm.chat_id_admin, text=message)
                if(status == "yes"):
                    #kirim file ke chat
                    try:
                        document = open("data//downloads//ReportServlet.xls","rb")
                        await context.bot.send_document(pm.chat_id_admin,document)
                        message = "Berhasil kirim File"
                        print(message)
                        await context.bot.send_message(
                            chat_id=pm.chat_id_admin, text=message)
                        break # Stop ketika sudah berhasil kirm file
                    except Exception as e:
                        message = "Gagal kirim file\nMessage Error : \n"+str(e)
                        await context.bot.send_message(
                            chat_id=pm.chat_id_admin, text="Gagal kirim file\n"+message)
                else:
                    await context.bot.send_message(
                        chat_id=pm.chat_id_admin, text="Gagal kirim file\n"+message)
            except:
                await context.bot.send_message(
                        chat_id=pm.chat_id_admin, text="Gagal mendownload laporan TS harian"+message)
                pass
            i += 1
    else:
        await context.bot.send_message(
            chat_id=pm.chat_id_admin, text="Gagal ambil kode unit\n"+message)
    # 2. Kirim Screenshoot laporan TS
    ii = 0
    while ii <3:
        await context.bot.send_message(
                chat_id=pm.chat_id_admin, text=f"Memulai kirim Rekap laporan TS Hari ini percobaan ke {ii+1}")
        try:
            [status,message] = Asmente.kirim_report_ts()
            if(status == "yes"):
                print(message)
                await context.bot.send_message(
                    chat_id=pm.chat_id_admin, text="Berhasil mengupdate Laporan TS P2TL pada spreadsheet")
                try:
                    document = open("fotoct//screenshot_ts.png","rb")
                    await context.bot.send_document(pm.chat_id_admin,document)
                    message = "Berhasil kirim Foto"
                    print(message)
                    await context.bot.send_message(
                        chat_id=pm.chat_id_admin, text=message)
                    break
                except Exception as e:
                    message = "Gagal kirim foto\nMessage Error : \n"+str(e)
                    print(message)
                    await context.bot.send_message(
                        chat_id=pm.chat_id_admin, text=message)
            else:
                await context.bot.send_message(
                    chat_id=pm.chat_id_admin, text=message)
        except:
            pass
        ii += 1
    #Proses pengiriman ke WA
    incoming_messages = dataframe.read_from_googlesheet_to_df(filepathjson=pm.filepathjson,GSHEET="NEW Monitoring Tindak Lanjut Harian JN Max UP3 MS 2024",TAB_NAME="DB",Cell="M3")
    message = Asmente.wa_sendMessage("Prioritas P2TL JN Max","Memulai mengirim laporan otomatis pada pukul : "+formatted_time)
    message = Asmente.wa_sendMessage("Prioritas P2TL JN Max",incoming_messages)
    await context.bot.send_message(
            chat_id=pm.chat_id_admin, text=incoming_messages)
    
async def update_realisasi_P2TL(context:CallbackContext):
    current_time = datetime.datetime.now()
    # Format the time string (optional)
    formatted_time = current_time.strftime("%H:%M:%S")  # Example: 20:11:13 (hour:minute:second)
    print(formatted_time)
    #Get current number of date
    # Set the locale to Indonesian for the month name
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
    # Get the current date
    current_date = datetime.datetime.now()
    # Format the date as "30 Juli 2024"
    formatted_date = current_date.strftime('%d %B %Y')
    #Mengirim notif bahwa proses update data laporan P2TL akan dimulai
    await context.bot.send_message(
        chat_id=pm.chat_id_laporandalsut, text=f"Memulai mengirim laporan TS P2TL pada pukul : {formatted_time}")
    df = dataframe()
    tahun_bulan = dataframe.get_tahun_bulan_sekarang() #jangan lupa jadikan variabel
    [status,kode_unit_user,message] = df.get_kode_unit_user_tagsus(chat_id=pm.chat_id_admin)
    if(status == "yes"):
        [status,message] = Asmente.create_lap_tsp2tl(kode_unit_user = kode_unit_user,tahun_bulan = tahun_bulan)
        await context.bot.send_message(
            chat_id=pm.chat_id_laporandalsut, text=message)
        if(status == "yes"):
            #kirim file ke chat
            try:
                document = open("data//downloads//ReportServlet.xls","rb")
                await context.bot.send_document(pm.chat_id_laporandalsut,document)
                message = "Berhasil kirim File"
                print(message)
                await context.bot.send_message(
                    chat_id=pm.chat_id_laporandalsut, text=message)
            except Exception as e:
                message = "Gagal kirim file\nMessage Error : \n"+str(e)
                await context.bot.send_message(
                    chat_id=pm.chat_id_laporandalsut, text="Gagal kirim file\n"+message)
            
            #kirim laporan
            [status,message] = Asmente.kirim_report_ts()
            await context.bot.send_message(
                    chat_id = pm.chat_id_laporandalsut , text="Berhasil mengupdate Laporan TS P2TL pada spreadsheet")
            try:
                document = open("fotoct//screenshot_ts.png","rb")
                await context.bot.send_document(pm.chat_id_laporandalsut,document)
                message = "Berhasil kirim Foto"
                print(message)
                await context.bot.send_message(
                    chat_id=pm.chat_id_laporandalsut, text=message)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=pm.chat_id_laporandalsut,
                                activity="Mengupdate laporan TS P2TL Sesuai Jadwal", time=str(datetime.datetime.now()))
            except Exception as e:
                message = "Gagal kirim foto\nMessage Error : \n"+str(e)
                print(message)
                await context.bot.send_message(
                    chat_id=pm.chat_id_laporandalsut, text=message)
        else:
            await context.bot.send_message(
                chat_id=pm.chat_id_laporandalsut, text="Gagal kirim file\n"+message)
    else:
        await context.bot.send_message(
            chat_id=pm.chat_id_laporandalsut, text="Gagal ambil kode unit\n"+message)

async def kirim_laporan_jnmax(context:CallbackContext):
    current_time = datetime.datetime.now()
    # Format the time string (optional)
    formatted_time = current_time.strftime("%H:%M:%S")  # Example: 20:11:13 (hour:minute:second)
    print(formatted_time)
    #Get current number of date
    # Set the locale to Indonesian for the month name
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

    # Get the current date
    current_date = datetime.datetime.now()

    # Format the date as "30 Juli 2024"
    formatted_date = current_date.strftime('%d %B %Y')

    #Mengirim notif bahwa proses update data laporan akan dimulai
    await context.bot.send_message(
        chat_id=pm.chat_id_laporandalsut, text=f"Memulai mengirim laporan JN max pada pukul : {formatted_time}")
    #Proses pengiriman ke WA
    incoming_messages = dataframe.read_from_googlesheet_to_df(filepathjson=pm.filepathjson,GSHEET="NEW Monitoring Tindak Lanjut Harian JN Max UP3 MS 2024",TAB_NAME="DB",Cell="M3")
    #message = Asmente.wa_sendMessage("Prioritas P2TL JN Max","Memulai mengirim laporan otomatis pada pukul : "+formatted_time)
    concatenate_report  = "Realisasi Tindak Lanjut Pelanggan 720 JN "+formatted_date+"\n"+"UP3...../Jumlah Tim / Jml P2TL (P1)/ Jml Tambah Daya / Kumulatif P1 / Kumulatif Tambah Daya\n"+incoming_messages
    #Kirim WA ke Grup TIndak Lanjut 720 JN UID
    message = Asmente.wa_sendMessage("Tindaklanjut pelanggan",concatenate_report)
    #Kirim laporan ke Bot Telegram
    await context.bot.send_message(
        chat_id=pm.chat_id_laporandalsut, text=incoming_messages)
    # Write log data
    dat = dataframe()
    dat.log_data(chat_id=pm.chat_id_laporandalsut,
                    activity="Mengirim Laporan Realisasi Tindak Lanjut JN Max Otomatis", time=str(datetime.datetime.now()))
    
async def kirim_laporan_jnmax_manual(update,context:CallbackContext):
    chat_id = update.message.chat_id
    current_time = datetime.datetime.now()
    # Format the time string (optional)
    formatted_time = current_time.strftime("%H:%M:%S")  # Example: 20:11:13 (hour:minute:second)
    print(formatted_time)
    #Get current number of date
    # Set the locale to Indonesian for the month name
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

    # Get the current date
    current_date = datetime.datetime.now()

    # Format the date as "30 Juli 2024"
    formatted_date = current_date.strftime('%d %B %Y')
    #Mengirim notif bahwa proses update data laporan akan dimulai
    await context.bot.send_message(
        chat_id=pm.chat_id_laporandalsut, text=f"Memulai mengirim laporan JN max pada pukul : {formatted_time}")
    #Proses pengiriman ke WA
    incoming_messages = dataframe.read_from_googlesheet_to_df(filepathjson=pm.filepathjson,GSHEET="NEW Monitoring Tindak Lanjut Harian JN Max UP3 MS 2024",TAB_NAME="DB",Cell="M3")
    message = Asmente.wa_sendMessage("Prioritas P2TL JN Max","Memulai mengirim laporan otomatis pada pukul : "+formatted_time)
    concatenate_report  = f"Realisasi Tindak Lanjut Pelanggan 720 JN\n{formatted_date}\nUP3...../Jumlah Tim / Jml P2TL (P1)/ Jml Tambah Daya / Kumulatif P1 / Kumulatif Tambah Daya\n{incoming_messages}"
    message = Asmente.wa_sendMessage("Prioritas P2TL JN Max",concatenate_report)
    await context.bot.send_message(
        chat_id=pm.chat_id_laporandalsut, text=incoming_messages)
    # Write log data
    dat = dataframe()
    dat.log_data(chat_id=pm.chat_id_laporandalsut,
                    activity="Mengirim Laporan Realisasi Tindak Lanjut JN Max Manual", time=str(datetime.datetime.now()))

async def update_spreadsheet_jnmax_uid(context:CallbackContext):
    current_time = datetime.datetime.now()
    # Format the time string (optional)
    formatted_time = current_time.strftime("%H:%M:%S")  # Example: 20:11:13 (hour:minute:second)
    print(formatted_time)
    #Mengirim notif bahwa proses update data laporan akan dimulai
    await context.bot.send_message(
        chat_id=pm.chat_id_laporandalsut, text=f"Memulai update Spreadsheet JN max UID : {formatted_time}")
    
    #Eksekusi update dengan menjalankan Appscript
    status = updatelaporan.run_spreadsheet_task()
    if(status):
        #kirim foto screenshoot
        updatelaporan.open_dashboard_uid()
        try:
            resp = requests.post("https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(pm.chat_id_laporandalsut), files=fm.send_photos("fotoct\\update_uid.png"))
        except:
            await context.bot.send_message(
                chat_id=pm.chat_id_laporandalsut, text=f"Gagal mengirim foto rekap")
    else:
        await context.bot.send_message(
                chat_id=pm.chat_id_laporandalsut, text=f"Gagal mengupdate data JN Max")

    # Write log data
    dat = dataframe()
    dat.log_data(chat_id=pm.chat_id_laporandalsut,
                    activity="mengupdate laporan spreadsheet monitoring JN Max UID Otomatis", time=str(datetime.datetime.now()))

async def update_spreadsheet_jnmax_uid_manual(update,context:CallbackContext):
    current_time = datetime.datetime.now()
    # Format the time string (optional)
    formatted_time = current_time.strftime("%H:%M:%S")  # Example: 20:11:13 (hour:minute:second)
    print(formatted_time)
    #Mengirim notif bahwa proses update data laporan akan dimulai
    await context.bot.send_message(
        chat_id=pm.chat_id_laporandalsut, text=f"Memulai update Spreadsheet JN max UID : {formatted_time}")
    status = updatelaporan.run_spreadsheet_task()
    if(status):
        #kirim foto screenshoot
        updatelaporan.open_dashboard_uid()
        try:
            resp = requests.post("https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(pm.chat_id_laporandalsut), files=fm.send_photos("fotoct\\update_uid.png"))
        except:
            await context.bot.send_message(
                chat_id=pm.chat_id_laporandalsut, text=f"Gagal mengirim foto rekap")
    else:
        await context.bot.send_message(
                chat_id=pm.chat_id_laporandalsut, text=f"Gagal mengupdate data JN Max")
    # Write log data
    dat = dataframe()
    dat.log_data(chat_id=pm.chat_id_laporandalsut,
                    activity="mengupdate laporan spreadsheet monitoring JN Max UID Manual", time=str(datetime.datetime.now()))
async def update_realisasi_kemarin(context:CallbackContext):
    current_time = datetime.datetime.now()
    # Format the time string (optional)
    formatted_time = current_time.strftime("%H:%M:%S")  # Example: 20:11:13 (hour:minute:second)
    print(formatted_time)
    #Mengirim notif bahwa proses update data laporan akan dimulai
    await context.bot.send_message(
        chat_id=pm.chat_id_laporandalsut, text=f"Memulai update realisasi TS Kemarin : {formatted_time}")
    #Update realisasi penetapan P1 kemarin (H-1)
    try:
        dataframe.update_realisasits_kemarin(filepathjson=pm.filepathjson,GSHEET="NEW Monitoring Tindak Lanjut Harian JN Max UP3 MS 2024",TAB_NAME="DB",CellRead="K5",CellWrite="H13")
        await context.bot.send_message(
            chat_id=pm.chat_id_laporandalsut, text=f"Berhasil Update data penetapan P1 H-1")
    except Exception as e:
        await context.bot.send_message(
            chat_id=pm.chat_id_laporandalsut, text=f"Gagal Update data P1\nMessage Error : {str(e)}")
    #Update realisasi PD Kemarin (H-1)
    try:
        dataframe.update_realisasits_kemarin(filepathjson=pm.filepathjson,GSHEET="NEW Monitoring Tindak Lanjut Harian JN Max UP3 MS 2024",TAB_NAME="DB",CellRead="K9",CellWrite="H18")
        await context.bot.send_message(
            chat_id=pm.chat_id_laporandalsut, text=f"Berhasil Update data Perubahan Daya H-1")
    except Exception as e:
        await context.bot.send_message(
            chat_id=pm.chat_id_laporandalsut, text=f"Gagal Update data P1\nMessage Error : {str(e)}")
    # Write log data
    dat = dataframe()
    dat.log_data(chat_id=pm.chat_id_laporandalsut,
                    activity="mengupdate Realisasi H-1 P1 dan PD", time=str(datetime.datetime.now()))
    

async def start_amicon(update,context):
    chat_id = update.message.chat_id
    reply_markup = AmiconBot.start()
    await context.bot.send_message(
            chat_id=chat_id, text="Silahkan pilih salah satu", reply_markup=reply_markup)
# Function to schedule the message
# Function to send a message


async def informasi(update, context):
    chat_id = update.message.chat_id
    [status, message] = Asmente.is_user_authenticated(chat_id=chat_id)
    if (status == "yes"):
        text1 = "1. Untuk mengakses *INFO PELANGGAN dengan idpel*, silahkan ketik :\n'Info|0|12 digit idpel , contoh Info|0|32131xxxxxxx'\nPencarian denga nomor meter 'Info|1|nomor meter' , contoh Info|1|450xxxxxxxx\n"
        text2 = "2. Untuk mengakses *INFO PELANGGAN via ACMT* dengan idpel. silahkan ketik 'Infoacmt|12 digit idpel' , contoh : Infoacmt 32111xxxxxxx\n"
        text3 = "3. Untuk mengakses *IINFO BLOCKING TOKEN dari AP2T* dengan idpel, silahkan ketik : Infoblokir|12 digit Idpel , contoh : Infoblokir|32121xxxxxxx\n"
        text4 = "4. Untuk mengakses *TOKEN KCT UPGRADE KRN* dengan idpel, silahkan ketik : Infokct idpel, contoh : Infokct 32131xxxxxxx\n"
        text5 = "5. Untuk *PEMBUATAN CT*, ketik 'Ct|12 Digit Idpel|kode unit|Keterangan (Penyebab periksa, petugas dan keterangan lainnya)'\ncontoh : Ct|32131xxxxxxx|32131|ganti mcb, petugas fulan\n"
        text6 = "6. Untuk *MENAMBAH USER BARU* (Hanya bisa di akses untuk role admin), ketik Add|chat id|kode unit|Nama User|Nomor Telfon|level user\nContoh : Add|817654873|32131|Fulan bin fulan|081321765487|user\n"
        text7 = "7. Untuk *REST IMEI HP ACMT petugas* Cater, ketik 'Resetimei|Kode unit|user petugas (tanpa kode uni)' , Contoh : Resetimei|32131|sitaba\n"
        text8 = "8. Untuk Cek *MONITORING PERMOHONAN TOKEN* berdasarkan Idpelnomor meter (kode 0 untuk idpel, 1 untuk nomor emter), 'ketik Montok|kode pencarian (0 / 1)|id pelanggan/nomor meter (sesuai dengan kategori)', contoh Montok|0|321500xxxxxx , atau Montok|1|14456787659\n"
        text9 = "9. Untuk cetak *KCT dari Nomor Agenda*, bisa ketik 'Cetakkct|18 digit Nomor Agenda' ,contoh : Cetakkct|321310054567857456\n"
        text10 = "10. Untuk cek *HISTORY PEMBELIAN PRABAYAR*, ketik 'Infotoken|12 digit Idpel', contoh : Infotoken|321114598716"
        text11 = "11. Untuk *CEK FOTO ACMT*foto 1 (Stand), foto 2, dan foto rumah di ACMT, ketik 'fotoacmt|12 digit idpel', contoh : fotoacmt|321114598716"
        text12 = "12. Untuk *DOWNLOAD LAP TS HARIAN* Harian, ketik 'tagsusp2tl' dan bot akan mendownlaod laporan TS hari tersebut realtime"
        text13 = "13. Untuk *MENGIRIM REPORT SERVLET* yang sudah di download pada fungsi 'tagsusp2tl', ketik 'kirimlapts'"
        text14 = "14. Untuk *DOWNLOAD LAPORAN TUL 309*, ketik 'Tul309|<kodeunit>|<tahun>|<bulan>|<jenis laporan (1. Untk Normal, 2.LPB, 3. TOTAL)>|<periode (bulanan/kumulatif)>\nContoh : Tul309|32151|2024|3|3|bulanan"
        text15 = "15. Untuk *UPDATE DATA USER* pada listuser, ketik update|<NIP>|<Kolom (1 Nama, 2 Jabatan,3 Password)> Contoh untk update password: Update|9009002F|3|Apr-24"
        text_penutup = "_*Info lebih lanjut silahkan hubungi Luthfil, TL DALSUT UP3 Makassar selatan*_"
        #merge_text = "Informasi cara pemakaian : \n"+text1+text2+text3+text4+text5+text6+text7+text8+text9+text10+text11+text12+text13+text_penutup
        text_merged = [text1,text2,text3,text4,text5,text6,text7,text8,text9,text10,text11,text12,text13,text14,text15,text_penutup]
        for i in range(len(text_merged)):
            print(f"Loop iteration: {i}")
            await context.bot.send_message(
                chat_id=chat_id, text=text_merged[i],parse_mode="Markdown")
    else:
        await context.bot.send_message(
            chat_id=chat_id, text=message)
        # notif ke admin
        await context.bot.send_message(
            chat_id=pm.chat_id_admin, text="Chatid tidak dikenal mencoba masuk")
        await context.bot.send_message(
            chat_id=pm.chat_id_admin, text=str(chat_id))

async def updateuser(update,context):         
    chat_id = update.message.chat_id
    [status, message] = Asmente.is_user_authenticated(chat_id=chat_id)
    if (status == "yes"):
        #cek level autentikasi User
        [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
        if (status == "yes" and (level_user == "owner" or level_user == "admin")):
            await context.bot.send_message(
                chat_id=chat_id, text="update|NIP(Angka dan Huruf Kapital|kode yang akan di update\n"+
                    "List Kode :\n"+
                    "1 : Kode unit\n2 : Nama\n3 : Jabatan\n4 : Password AP2T\nContoh jika akan mengupdate Password\n"+
                    "update|1234567ZY|4")
            await context.bot.send_message(
                chat_id=chat_id, text="update|94171287ZY|4")
        else:
            await context.bot.send_message(
                chat_id=chat_id, text="Mengupdate user hanya untuk role Owner dan Admin, silahkan kontak Luthfil")
    else:
        await context.bot.send_message(
            chat_id=chat_id, text=message)
        # notif ke admin
        await context.bot.send_message(
            chat_id=pm.chat_id_admin, text="Chatid tidak dikenal mencoba masuk")
        await context.bot.send_message(
            chat_id=pm.chat_id_admin, text=str(chat_id))
        
def findnth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)
def get_result(value):
    result_dict = {
        "1": 'kodeunit',
        "2": 'jabatan',
        "3": 'password',
    }
    return result_dict.get(value, 'Invalid value')
# List perintah Asmen TE


async def button(update, context):
    query = update.callback_query
    await context.bot.send_message(text="Yang dipilih : %s" %
                             query.data, chat_id=query.message.chat_id)
    message = ReplyButton.execute_button(
        data=query.data, kode_unit="32131")
    # Coba kirim respon
    await context.bot.send_message(
        chat_id=query.message.chat_id, text=message)


async def read_command(update, context):
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
                await context.bot.send_message(
                    chat_id=chat_id, text="Memulai pembuatan CT Idpel : \n"+update.message.text[3:15]+"\nKode Unit : "+update.message.text[16:21]+"\nKeterangan : "+update.message.text[22:])
                status, jumlahct, message = Asmente.buatCT(
                    id_pelanggan=update.message.text[3:15], kodeunit=update.message.text[16:21], keteranganCT=update.message.text[22:])
                if (status == "yes"):
                    print("STATUS MAIN : ", message)
                    # Kirim jumlah permintaan CT
                    await context.bot.send_message(
                        chat_id=chat_id, text="Jumlah Permintaan CT : "+str(jumlahct))
                    await context.bot.send_message(chat_id=chat_id, text=message)
                    time.sleep(2)
                    resp = requests.post(
                        "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(chat_id), files=fm.send_photos(pm.files_foto_ct))
                    # Write log data
                    dat = dataframe()
                    dat.log_data(chat_id=chat_id,
                                 activity="clear tamper idpel :"+update.message.text[3:15], time=str(datetime.datetime.now()))
                else:
                    print("STATUS MAIN : ", message)
                    await context.bot.send_message(chat_id=chat_id, text=message)
            elif (status_kdunit == "no"):
                await context.bot.send_message(
                    chat_id=chat_id, text=message_kdunit)
        elif ((update.message.text[:4] == "info" and update.message.text[4:5] == "|") or (update.message.text[:4] == "Info" and update.message.text[4:5] == "|") or (update.message.text[:4] == "INFO" and update.message.text[4:5] == "|")):
            if (update.message.text[5:6] == "0"):
                await context.bot.send_message(
                    chat_id=chat_id, text="Memulai Pencarian Informasi Idpel : \n"+update.message.text[7:])
                [status, informasi, message] = Asmente.cek_infopelanggan(
                    tipe_pencarian="Id Pelanggan", nomor_id=update.message.text[7:], link_infopelanggan=pm.link_info_pelanggan)
                await context.bot.send_message(
                    chat_id=chat_id, text="Info Pelanggan berdasarkan Id Pelanggan :\n"+informasi)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                             activity="Info Pelanggan", time=str(datetime.datetime.now()))
            elif (update.message.text[5:6] == "1"):
                await context.bot.send_message(
                    chat_id=chat_id, text="Memulai Pencarian Informasi Nomor Meter :\n"+update.message.text[7:])
                [status, informasi, message] = Asmente.cek_infopelanggan(
                    tipe_pencarian="Nomor Meter", nomor_id=update.message.text[7:], link_infopelanggan=pm.link_info_pelanggan)
                await context.bot.send_message(
                    chat_id=chat_id, text="Info Pelanggan berdasarkan Nomor Meter \n:"+informasi)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                             activity="Info Pelanggan", time=str(datetime.datetime.now()))
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text="Tipe Pencarian tidak ditemukan")
        elif (update.message.text[:8] == "infoacmt" and update.message.text[8:9] == "|" or update.message.text[:8] == "Infoacmt" and update.message.text[8:9] == "|" or update.message.text[:8] == "INFOACMT" and update.message.text[8:9] == "|"):
            await context.bot.send_message(
                chat_id=chat_id, text="Memulai pengecekan Info pelanggan ACMT idpel : "+update.message.text[9:])
            [status, informasi, message] = Asmente.info_pelanggan_acmt(
                id_pelanggan=update.message.text[9:])
            await context.bot.send_message(
                chat_id=chat_id, text=informasi)
            await context.bot.send_message(
                chat_id=chat_id, text=message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                         activity="Info ACMT", time=str(datetime.datetime.now()))
        elif (update.message.text[:9] == "resetimei" or update.message.text[:9] == "Resetimei" or update.message.text[:9] == "RESETIMEI"):
            id_input = update.message.text[16:]
            kode_unit = update.message.text[10:15]
            await context.bot.send_message(
                chat_id=chat_id, text="Memulai reset imei petugas id : "+kode_unit+"."+id_input)
            [status, message] = Asmente.reset_imei(
                kode_unit=kode_unit, user_id=id_input)
            if (status == "yes"):
                await context.bot.send_message(
                    chat_id=chat_id, text=message)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                             activity="reset imei", time=str(datetime.datetime.now()))
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text=message)
        elif ((update.message.text[:6] == "montok" or update.message.text[:6] == "Montok" or update.message.text[:6] == "MONTOK") and len(update.message.text) > 18):
            # cek tipe pencarian
            tipe_pencarian = update.message.text[7:8]
            id_pencarian = update.message.text[9:]
            if (tipe_pencarian == "0"):
                await context.bot.send_message(
                    chat_id=chat_id, text="Memulai monitoring permohonan token Idpel : "+id_pencarian)
                status, message = Asmente.info_montok(
                    url_montok=pm.link_montok, tipe_pencarian=tipe_pencarian, id_pencarian=id_pencarian)
                if (status == "yes"):
                    await context.bot.send_message(
                        chat_id=chat_id, text="Hasil monitoring permohonan token Id pelanggan : "+id_pencarian+"\n"+message)
                else:
                    await context.bot.send_message(
                        chat_id=chat_id, text="Gagal monitoring permohonan token Id pelanggan : "+id_pencarian+"\n"+message)
            elif (tipe_pencarian == "1"):
                await context.bot.send_message(
                    chat_id=chat_id, text="Memulai monitoring permohonan token Nomor Meter : "+id_pencarian)
                status, message = Asmente.info_montok(
                    url_montok=pm.link_montok, tipe_pencarian=tipe_pencarian, id_pencarian=id_pencarian)
                if (status == "yes"):
                    await context.bot.send_message(
                        chat_id=chat_id, text="Hasil monitoring permohonan token Nomor meter : "+id_pencarian+"\n"+message)
                else:
                    await context.bot.send_message(
                        chat_id=chat_id, text="Gagal monitoring permohonan token Nomor Meter : "+id_pencarian+"\n"+message)
            else:
                await context.bot.send_message(
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
                await context.bot.send_message(
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
                await context.bot.send_message(
                    chat_id=pm.chat_id_admin, text="Memulai add user dengan chat id : "+str(chat_id_daftar)+"\n"+"Kode Unit : "+str(update.message.text[separator_1+1:separator_2]))
                [status, message] = Asmente.add_new_user(
                    chat_id_daftar=chat_id_daftar, kode_unit=int(update.message.text[separator_1+1:separator_2]), nama=nama, nomor_telfon=nomor_telfon, level=update.message.text[separator_4+1:])
                await context.bot.send_message(
                    chat_id=pm.chat_id_admin, text=message)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                             activity="Add user", time=str(datetime.datetime.now()))
            else:
                await context.bot.send_message(
                    chat_id=update.message.chat_id, text="User tidak punya hak akses")
        elif (len(update.message.text) == 20 and (update.message.text[:7] == "Infokct" or update.message.text[:7] == "infokct")):
            await context.bot.send_message(
                chat_id=update.message.chat_id, text="Memulai cek info KCT KRN Idpel : "+update.message.text[8:])
            [status, message] = Asmente.get_kct_krn(
                Id_pelanggan=update.message.text[8:])
            await context.bot.send_message(
                chat_id=update.message.chat_id, text=message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                         activity="Infokct krn", time=str(datetime.datetime.now()))
        elif (update.message.text[:10] == "Infoblokir" or update.message.text[:10] == "infoblokir"):
            await context.bot.send_message(
                chat_id=chat_id, text="Memulai pengecekan blocking token idppel : "+update.message.text[11:])
            status, message = Asmente.cek_blocking_token(
                id_pelanggan=update.message.text[11:])
            await context.bot.send_message(
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
                await context.bot.send_message(
                    chat_id=chat_id, text="Memulai pencarian history pembelian token Idpel "+id_pelanggan+" : ")
                [status,informasi,message] = Asmente.cek_pembelian_token(id_pelanggan)
                if(status=="yes"):
                    await context.bot.send_message(
                        chat_id=chat_id, text=informasi)
                else:
                    await context.bot.send_message(
                        chat_id=chat_id, text=message)
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text="Periksa idpel dengan benar")
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                            activity="Info Pembelian token", time=str(datetime.datetime.now()))
        elif ((update.message.text[:8] == "cetakkct" or update.message.text[:8] == "Cetakkct" or update.message.text[:8] == "CETAKKCT") and len(update.message.text) > 25):
            await context.bot.send_message(
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
                    await context.bot.send_message(
                        chat_id=chat_id, text="Gagal kirim screenshoot token\nError Meesage : "+message)
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text="Gagal cetak token\nError Meesage : "+message)
        #Fungsi Manajemen User
        elif ((update.message.text[:9] == "broadcast" or update.message.text[:9] == "Broadcast") and update.message.text[9:10] == "|"):
            # cek level user
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "owner" or level_user == "admin")):
                await context.bot.send_message(
                    chat_id=chat_id, text="Memulai mengirim pesan broadcast")
                df = dataframe.get_all_userid(pm.filepathlistuser, "all")
                pesan = update.message.text[(findnth(
                    update.message.text, "|", 1)+1):]
                for i in df:
                    # print("chat id : ", str(i))
                    try:
                        await context.bot.send_message(
                            chat_id=i, text="Pesan Broadcast dari Admin : ")
                        await context.bot.send_message(
                            chat_id=i, text=pesan+"\n\n"+update.message.text[findnth(update.message.text, "|", 0)+1:findnth(update.message.text, "|", 1)])
                        # Write log data
                        dat = dataframe()
                        dat.log_data(chat_id=chat_id,
                                     activity="Broadcast by : "+chat_id, time=str(datetime.datetime.now()))
                    except:
                        pass
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text="Level user tidak memiliki autentikasi")
        elif((update.message.text[:7] == "update|" or update.message.text[:7] == "Update|" or update.message.text[:7] == "UPDATE|") and len(update.message.text) > 10):
            #cek level autentikasi User
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "owner" or level_user == "admin")):
                separator_2 = findnth(update.message.text, "|", 2)
                input_value = str(update.message.text[7:separator_2-2])#baru tambah
                update_value = update.message.text[(separator_2+1):]
                item_update = get_result(update.message.text[separator_2-1])
                print(update.message.text[separator_2-1])
                await context.bot.send_message(
                    chat_id=chat_id, text="Memulai Update "+item_update+" User NIP "+input_value)
                column_objective = "B"
                if(item_update == "jabatan"):
                    column_objective = "D"
                elif(item_update == "password"):
                    column_objective = "E"
                else:
                    column_objective = "B"
                daf = dataframe()
                [status, message]=daf.update_user_data(filepathlistuser=pm.filepathlistuser,sheetname="Sheet1",column_lookup="NIP",input_value=input_value,updated_value=update_value,column_objective=column_objective)#ubah nilai dari param input_value dengan nilai variabel input_value
                await context.bot.send_message(
                    chat_id=pm.chat_id_admin, text=message)
                daf.log_data(chat_id=chat_id,
                             activity="Update "+ item_update + " User dengan NIP "+ input_value, time=str(datetime.datetime.now()))
            else:
                await context.bot.send_message(
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
                    await context.bot.send_message(
                        chat_id=chat_id, text="Memulai Aktivasi kWh Meter\nIdpel : "+id_pelanggan+"\nKode Unit : "+update.message.text[10:15]+"\nNomor Meter Lama : "+nomor_meter_lama+"\nKeterangan : "+keterangan)
                    [status, message, nomoragenda] = Asmente.buatPengaduanHarAPP(
                        id_pelanggan=id_pelanggan, kode_unit=kodeunit, nomor_meter_lama=nomor_meter_lama, keterangan=keterangan)
                    if (status == "yes" and nomoragenda != 0):
                        await context.bot.send_message(
                            chat_id=chat_id, text="tindakan|"+kodeunit+"|"+str(nomoragenda))
                    else:
                        await context.bot.send_message(
                            chat_id=chat_id, text="Gagal buat pengaduan\nMessage Error : "+message)
                    # Write log data
                    dat = dataframe()
                    dat.log_data(chat_id=chat_id,
                                 activity="Buat pengaduan APP Idpel : "+id_pelanggan, time=str(datetime.datetime.now()))
                else:
                    await context.bot.send_message(
                        chat_id=chat_id, text="Kode Unit user tidak sesuai")
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text="User tidak punya hak akses")
        elif ((update.message.text[:8] == "tindakan" or update.message.text[:8] == "Tindakan" or update.message.text[:8] == "TINDAKAN") and len(update.message.text) == 33):
            kode_unit = update.message.text[9:14]
            nomoragenda = update.message.text[15:]
            await context.bot.send_message(
                chat_id=chat_id, text="Memulai save tindakan pengaduan\nNomor Agenda : "+nomoragenda+"\nKode Unit : "+kode_unit)
            status, message, nomoragenda = Asmente.tindakanPengaduanHarAPP(
                nomoragenda=int(nomoragenda), kode_unit=kode_unit)
            if (status == "yes"):
                await context.bot.send_message(
                    chat_id=chat_id, text="Berhasil save tindakan pengaduan Nomor Agenda " +
                    str(nomoragenda))
                await context.bot.send_message(
                    chat_id=chat_id, text="aktivasiapp|"+kode_unit+"|"+str(nomoragenda)+"|"+"Nomor Meter Baru")
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text=message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                         activity="Save tindakan pengaduan Agenda: "+str(nomoragenda), time=str(datetime.datetime.now()))
        elif ((update.message.text[:11] == "aktivasiapp" or update.message.text[:11] == "Aktivasiapp" or update.message.text[:11] == "AKTIVASIAPP") and len(update.message.text) == 48):
            kode_unit = update.message.text[12:17]
            nomoragenda = update.message.text[18:36]
            nomor_meter_baru = update.message.text[37:]
            await context.bot.send_message(
                chat_id=chat_id, text="Memulai aktivasi kWh meter dengan nomor agenda : "+nomoragenda+"\nNomor meter baru : "+nomor_meter_baru+"\nKode Unit : "+kode_unit)
            status, message, nomoragenda = Asmente.aktivasiHarAPP(nomoragenda=int(
                nomoragenda), kode_unit=kode_unit, nomor_meter_baru=nomor_meter_baru)
            if (status == "yes" and nomoragenda != 0):
                await context.bot.send_message(
                    chat_id=chat_id, text="cetakkct|"+str(nomoragenda))
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text=message)
        elif ((update.message.text[:10] == "tagsusp2tl" or update.message.text[:10] == "Tagsusp2tl" or update.message.text[:10] == "TAGSUSP2TL")):
            #cek level autentikasi User
            [status, level_user, message] = Asmente.get_level_user(
                chat_id=chat_id)
            if (status == "yes" and (level_user == "owner" or level_user == "admin")):
                await context.bot.send_message(
                        chat_id=chat_id, text="Memulai Pembuatan Laporan Tagihan Susulan Hari ini")
                df = dataframe()
                tahun_bulan = dataframe.get_tahun_bulan_sekarang() #jangan lupa jadikan variabel
                [status,kode_unit_user,message] = df.get_kode_unit_user_tagsus(chat_id=chat_id)
                if(status == "yes"):
                    [status,message] = Asmente.create_lap_tsp2tl(kode_unit_user = kode_unit_user,tahun_bulan = tahun_bulan)
                    await context.bot.send_message(
                        chat_id=chat_id, text=message)
                    if(status == "yes"):
                        #kirim file ke chat
                        try:
                            document = open("data//downloads//ReportServlet.xls","rb")
                            await context.bot.send_document(chat_id,document)
                            message = "Berhasil kirim File"
                            print(message)
                            await context.bot.send_message(
                                chat_id=chat_id, text=message)
                        except Exception as e:
                            message = "Gagal kirim file\nMessage Error : \n"+str(e)
                            await context.bot.send_message(
                                chat_id=chat_id, text="Gagal kirim file\n"+message)
                    else:
                        await context.bot.send_message(
                            chat_id=chat_id, text="Gagal kirim file\n"+message)
                else:
                    await context.bot.send_message(
                        chat_id=chat_id, text="Gagal ambil kode unit\n"+message)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                                activity="Update Laporan TS Harian", time=str(datetime.datetime.now()))
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text="Update Laporan Harian hanya untuk level Admin atau Owner")
        elif((update.message.text[:8] == "fotoacmt" or update.message.text[:8] == "Fotoacmt" or update.message.text[:8] == "FOTOACMT") and len(update.message.text) == 21):
            idpel = update.message.text[9:]
            await context.bot.send_message(
                chat_id=chat_id, text="Memulai kirim foto ACMT Idpel "+idpel)
            status1,status2,statusrumah = Asmente.get_foto_rumah(idpelanggan=idpel)
            if(statusrumah == "yes"):
                resp = requests.post(
                            "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(chat_id), files=fm.send_photos(pm.files_foto_rumah))
                await context.bot.send_message(
                    chat_id=chat_id, text="Foto Rumah Berhasil di kirim")
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text="Gagal get foto rumah")
            if(status1 == "yes"):
                resp = requests.post(
                            "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(chat_id), files=fm.send_photos(pm.files_foto_1))
                await context.bot.send_message(
                    chat_id=chat_id, text="Foto 1 Berhasil di kirim")
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text="Gagal kirim foto 1")
            if(status2 == "yes"):
                resp = requests.post(
                            "https://api.telegram.org/bot"+pm.tokenbot+"/sendPhoto?chat_id="+str(chat_id), files=fm.send_photos(pm.files_foto_2))
                await context.bot.send_message(
                    chat_id=chat_id, text="Foto 2 Berhasil di kirim")
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text="Gagal kirim foto rumah")
            
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                            activity="Foto ACMT idpel : "+idpel, time=str(datetime.datetime.now()))          
        elif((update.message.text[:10] == "kirimlapts" or update.message.text[:10] == "Kirimlapts" or update.message.text[:10] == "KIRIMLAPTS")):
            await context.bot.send_message(
                chat_id=chat_id, text="Memulai kirim laporan TS Hari ini")
            [status,message] = Asmente.kirim_report_ts()
            if(status == "yes"):
                print(message)
                await context.bot.send_message(
                    chat_id=chat_id, text="Berhasil mengupdate Laporan TS P2TL pada spreadsheet")
                try:
                    document = open("fotoct//screenshot_ts.png","rb")
                    await context.bot.send_document(chat_id,document)
                    message = "Berhasil kirim Foto"
                    print(message)
                    await context.bot.send_message(
                        chat_id=chat_id, text=message)
                except Exception as e:
                    message = "Gagal kirim foto\nMessage Error : \n"+str(e)
                    print(message)
                    await context.bot.send_message(
                        chat_id=chat_id, text=message)
            else:
                await context.bot.send_message(
                    chat_id=chat_id, text=message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                            activity="Kirim Laporan TS Harian", time=str(datetime.datetime.now()))
        elif((update.message.text[:6] == "tul309" or update.message.text[:6] == "Tul309" or update.message.text[:6] == "TUL309")):
            #Definisikan posisi separator
            separator_1 = findnth(update.message.text, "|",0)
            separator_2 = findnth(update.message.text,"|",1)
            separator_3 = findnth(update.message.text,"|",2)
            separator_4 = findnth(update.message.text,"|",3)
            separator_5 = findnth(update.message.text,"|",4)
            kdunit = update.message.text[separator_1+1:separator_2]
            tahun = update.message.text[separator_2+1:separator_3]
            bulan = update.message.text[separator_3+1:separator_4]
            jenislaporan = update.message.text[separator_4+1:separator_5]
            tipelaporan = update.message.text[separator_5+1:]
            nama_jenislaporan = ""
            #Set jenis laporan to string
            if(jenislaporan == "1"):
                nama_jenislaporan = "NORMAL"
            elif(jenislaporan == "2"):
                nama_jenislaporan = "LPB"
            else:
                nama_jenislaporan = "TOTAL"
            await context.bot.send_message(
                chat_id=chat_id, text=f"Memulai download Laporan TUL 309 Kode Unit :{kdunit}\nBulan : {bulan} \nTahun : {tahun} \nJenis Laporan : {jenislaporan} {nama_jenislaporan}")
            
            [status,message] = Asmente.kirim_tul309(link_TUL309="any",kdunit=int(kdunit),tahun=tahun,bulan=bulan,jenislaporan=jenislaporan,tipelaporan=tipelaporan)
            if(status == "yes"):
                path = "data//downloads"
                
                status,most_recent_files = filemanager.select_last_modified_files(path=path)
                #Try to rename the most recent downloaded file
                new_filename_with_extension = f"TUL 309 ULP {kdunit} Bulan {bulan} Tahun {tahun} {nama_jenislaporan} {tipelaporan}.xls" #prepare for the new name file extension
                #Delete the same file if it was existed
                [status,message] = filemanager.delete_file(folder_path=path,filename_and_name_extension=new_filename_with_extension)
                if(status == "yes"):
                    print("File lama berhasil di hapus")
                else:
                    print("File yang sama tidak ditemukan")
                try:
                    #Rename the file
                    status,most_recent_files,message = filemanager.rename_most_recent_file(path=path,most_recent_file=most_recent_files,new_file_name_with_extension=new_filename_with_extension)
                    if(status == "yes"):
                        try:
                            #Try to send the file
                            status,most_recent_files = filemanager.select_last_modified_files(path=path)
                            document = open(path+"//"+most_recent_files,"rb")
                            await context.bot.send_document(chat_id,document)
                            message = "Berhasil kirim File"
                            print(message)
                            await context.bot.send_message(
                                chat_id=chat_id, text=message)
                        except Exception as e:
                            message = "Gagal kirim file\n"+message+"\nMessage Error : \n"+str(e)
                            await context.bot.send_message(
                                chat_id=chat_id, text="Gagal kirim file\n"+message)
                    else:
                        await context.bot.send_message(
                                chat_id=chat_id, text="Gagal Rename file\n"+message)
                except Exception as e:
                    message = "Gagal rename FIle\nMessage Error : \n"+str(e)
                # Write log data
                dat = dataframe()
                dat.log_data(chat_id=chat_id,
                                activity="Mendowload Laporan TUL 309", time=str(datetime.datetime.now()))
            else:
                await context.bot.send_message(
                        chat_id=chat_id, text="Gagal kirim file\n"+message)
        #KIRIM LAPORAN EXCEL TAMBAH DAYA
        elif((update.message.text[:9] == "laporanpd") or (update.message.text[:9] == "Laporanpd")):
            await context.bot.send_message(chat_id=chat_id,text="Memulai mengupdate laporan PD dari EIS")
            message_update = Asmente.update_data_pd()
            await context.bot.send_message(chat_id=chat_id,text=message_update)
               #kirim file ke chat
            try:
                #document = open("data//downloads//EIS//GV.xls","rb")
                #wait context.bot.send_document(chat_id,document)
                message = "Berhasil kirim File"
                print(message)
                await context.bot.send_message(
                    chat_id=chat_id, text=message)
            except Exception as e:
                message = "Gagal kirim file\nMessage Error : \n"+str(e)
                await context.bot.send_message(
                    chat_id=chat_id, text="Gagal kirim file\n"+message)
        #Fungsi Bot AMICON Register Asset dan Comissioning
        #Asset
        elif((update.message.text[:] == "ASSET")):
            message = update.message.text[:]
            bot = AmiconBot()
            bot.get_first_choice(message=message)
            await context.bot.send_message(
                chat_id=chat_id, text="Silahkan Pilih Tipe Aset : ", reply_markup=bot.set_asset_choice())
        elif((update.message.text[:] == "METER")):
            message = update.message.text[:]
            bot = AmiconBot()
            bot.get_selected_asset(selected_aset=message)
            await context.bot.send_message(
                chat_id=chat_id, text="Silahkan Pilih Tipe Merk : ", reply_markup=bot.set_meter_brand())
        elif(update.message.text[:] == "EDMI"):
            message = update.message.text[:]
            bot = AmiconBot()
            bot.get_selected_brand(selected_brand=message)
            await context.bot.send_message(
                chat_id=chat_id, text="Silahkan Pilih Tipe Merk : ", reply_markup=bot.set_brand_type(selected_brand=message))
        elif(update.message.text[:] == "ITRON"):
            message = update.message.text[:]
            bot = AmiconBot()
            bot.get_selected_brand(selected_brand=message)
            await context.bot.send_message(
                chat_id=chat_id, text="Silahkan Pilih Tipe Merk : ", reply_markup=bot.set_brand_type(selected_brand=message))
        #Comissioning
        elif(update.message.text[:] == "COMISSIONING"):
            message = "COMMISSIONING|32XXXXXXXXXX"
            await context.bot.send_message(
                chat_id=chat_id, text=message)
        elif(update.message.text[:12] == "COMISSIONING" and len(update.message.text)> 20):
            idpel = update.message.text[13:]
            await context.bot.send_message(
                chat_id=chat_id, text="Memulai Comissioning Pelanggan ID : "+idpel)
            amicon = Amicon(username=pm.username_amicon,password=pm.password_amicon)
            amicon.first_page()
            status_login,message = amicon.cek_login()
            result = ""
            if(status_login == "no"):
                print(message)
                await context.bot.send_message(
                chat_id=chat_id, text="Memulai Login")
                #Login
                amicon.login()
                [status,message] = amicon.cek_login()
                #Cek apakah berhasil login
                if(status == "no"):
                    await context.bot.send_message(
                        chat_id=chat_id, text="Gagal Login ke AMICON, periksa username dan password/Captcha")
            #Berhasil login, lanjut buka Menu COmissioning
            await context.bot.send_message(
                        chat_id=chat_id, text="Berhasil Login")
            status_menu_comiss = True
            counter = 0
            #Lakukan 5x percobaan untuk click menu comissioning
            while status_menu_comiss:
                [status_menu_comiss,message] = amicon.click_comissioning()
                print(message)
                time.sleep(5)
                counter = counter+1
                if(counter > 15):
                    break
            if(status_menu_comiss == False):
                await context.bot.send_message(
                        chat_id=chat_id, text="Berhasil masuk ke menu comissioning")
                status = amicon.click_search_idpel_comissioning(idpel=idpel)
                #Pelanggan di temukan dan dilakukan comissioning
                await context.bot.send_message(
                    chat_id=chat_id, text="Pelanggan ditemukan dan dilakukan comissioning, silahkan ditunggu hingga proses comissioning berhasil")
                if(status):
                    await context.bot.send_message(
                        chat_id=chat_id, text="Berhasil comissioning, semua status OK, lanjut verifiy test")      
                    #try click verify
                    condition = True
                    counter = 0
                    #Klik verify test jika comissionng telah selesai sampai semua step OK
                    while condition:
                        condition = amicon.click_verify_test()
                        time.sleep(5)
                        counter = counter + 1
                        if(counter > 50):
                            break
                    if(condition == False):
                        await context.bot.send_message(
                            chat_id=chat_id, text="Berhasil Verify Test")
                        #klik pop up verify
                        condition = True
                        counter = 0
                        while condition:
                            condition = amicon.click_popup_verify()
                            time.sleep(5)
                            counter = counter + 1
                            if(counter > 50):
                                break
                        #Jika Berhasil klik pop up verify
                        if(condition == False):
                            await context.bot.send_message(
                                chat_id=chat_id, text="Berhasil klik Pop Up Verify,lanjut Activation")
                            #Confirm activate
                            condition = True
                            counter = 0
                            while condition:
                                condition = amicon.click_confirm_activate()
                                time.sleep(5)
                                counter = counter + 1
                                if(counter > 50):
                                    break
                            if(condition == False):
                                await context.bot.send_message(
                                    chat_id=chat_id, text="Berhasil klik Confirm Activate")
                                #Pop Up Confirm activate
                                condition = True
                                counter = 0
                                while condition:
                                    condition = amicon.click_confirm_popup_activate()
                                    time.sleep(5)
                                    counter = counter + 1
                                    if(counter > 50):
                                        break
                                if(condition == False):
                                    await context.bot.send_message(
                                        chat_id=chat_id, text="Berhasil klik Confirm pop Up Activate\nSIlahkan tunggu sampai selesai Activate dan donwload ComissioningResult")
                                    condition = True
                                    loop_value = 0
                                    while condition:
                                        print("Klik Download PDF")
                                        condition = amicon.click_download_pdf_comissioning()
                                        time.sleep(5)
                                        loop_value = loop_value + 1
                                        if(loop_value > 50):
                                            break
                                    if(condition == False):
                                        #Jika download berhasil, lanjut mengirim FIle ComissioningResult
                                        await context.bot.send_message(
                                            chat_id=chat_id, text="Berhasil download ComissioningResult, Mengirim File\nSIlahkan Tunggu")
                                        path = "data//downloads"
                                        status,most_recent_files = filemanager.select_last_modified_files(path=path)
                                        try:
                                            document = open(path+"//"+most_recent_files,"rb")
                                            await context.bot.send_document(chat_id,document)
                                            message = "Berhasil kirim File"
                                            print(message)
                                            await context.bot.send_message(
                                                chat_id=chat_id, text=message)
                                            #Klik Finish jika sudah kirim FIle
                                            condition = True
                                            loop_value = 0
                                            while condition:
                                                print("Klik Download PDF")
                                                condition = amicon.click_finish_comissioning()
                                                time.sleep(5)
                                                loop_value = loop_value + 1
                                                if(loop_value > 5):
                                                    break
                                            if(condition == False):
                                                await context.bot.send_message(
                                                    chat_id=chat_id, text="Berhasil Click Finish\nProses Comissioning Selesai")
                                            else:
                                                await context.bot.send_message(
                                                    chat_id=chat_id, text="Gagal klik Finish")
                                        except Exception as e:
                                            message = "Gagal kirim file\nMessage Error : \n"+str(e)
                                            await context.bot.send_message(
                                                chat_id=chat_id, text="Gagal kirim file\n"+message)
                                    else:
                                        await context.bot.send_message(
                                            chat_id=chat_id, text="Gagal Download Comissioning result")
                                else:
                                    await context.bot.send_message(
                                        chat_id=chat_id, text="Gagal klik pop up COnfirm Activate")
                            else:
                                await context.bot.send_message(
                                    chat_id=chat_id, text="Gagal klik konfirm pop up verify")
                        else:
                            await context.bot.send_message(
                                chat_id=chat_id, text="Gagal pilih pop up verify")
                    else:
                        await context.bot.send_message(
                            chat_id=chat_id, text="Gagal comissioning, tidak dapat menyelesaikan semua step")
                else:
                    await context.bot.send_message(
                        chat_id=chat_id, text="Comissioning gagal dimulai, pastikan idpel yang di input benar")
            else:
                await context.bot.send_message(
                        chat_id=chat_id, text=message)
            
            # #Menunggu proses download
            # time.sleep(10)
            # if(result == "success"):
            #     context.bot.send_message(
            #     chat_id=chat_id, text="Berhasil melakukan Comissioning Idpel : "+idpel)
            #     path = "data//downloads"
            #     status,most_recent_files = filemanager.select_last_modified_files(path=path)
            #     try:
            #         document = open(path+"//"+most_recent_files,"rb")
            #         context.bot.send_document(chat_id,document)
            #         message = "Berhasil kirim File"
            #         print(message)
            #         context.bot.send_message(
            #             chat_id=chat_id, text=message)
            #     except Exception as e:
            #         message = "Gagal kirim file\nMessage Error : \n"+str(e)
            #         context.bot.send_message(
            #             chat_id=chat_id, text="Gagal kirim file\n"+message)
            # else:
            #     context.bot.send_message(
            #             chat_id=chat_id, text="Gagal Comissioning"+message)
            # Write log data
            dat = dataframe()
            dat.log_data(chat_id=chat_id,
                            activity="Comissioning : "+idpel, time=str(datetime.datetime.now()))
        else:
            print("command tidak dikenal")
            await context.bot.send_message(
                chat_id=chat_id, text="command tidak dikenal")
    else:
        print(message)
        # notif ke user
        await context.bot.send_message(
            chat_id=chat_id, text=message)
        # notif ke admin
        await context.bot.send_message(
            chat_id=pm.chat_id_admin, text="Chatid tidak dikenal mencoba masuk")
        await context.bot.send_message(
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


async def update_data_otomatis(context: CallbackContext):
    """Fungsi ini membuat Thread untuk update masing2 UP3"""
    try:
        s = time.perf_counter()
        bot = Amicon(username=pm.username_amicon,
                     password=pm.password_amicon)
        bot.download_data(get_gardu())
        f = time.perf_counter()
        waktu = round((f - s), 2)
        await context.bot.send_message(text=f'Berhasil update data Gardu dari AMICON ({waktu}s)',
                                 reply_markup='markdown')
    except Exception as e:
        await context.bot.send_message(
            text='Gagal Update data Gardu dari AMICON',
            parse_mode='markdown')
        return


def main():
    # bot Telegram
    # Create updater and pass in Bot's auth key.
    #updater = Updater(token=pm.tokenbot, use_context=True)
    application = Application.builder().token(pm.bot_token).build()
    # Get dispatcher to register handlers
    #dispatcher = updater.dispatcher
    # Mengecek kesiapan bot
    application.add_handler(CommandHandler(
        'start', start))
    # Mengecek kesiapan bot
    application.add_handler(CommandHandler(
        'informasi', informasi))
    # Mengecek kesiapan bot
    application.add_handler(CommandHandler(
        'updateuser', updateuser))
    application.add_handler(CommandHandler('kirim_laporan_jnmax',kirim_laporan_jnmax_manual))
    #Run update Spreadsheet Monitoring JN max UID
    application.add_handler(CommandHandler('update_spreadsheet_jnmax_uid',update_spreadsheet_jnmax_uid_manual))
    # Run Aplikasi si gadis
    application.add_handler(CommandHandler('start_sigadis', start_sigadis))
    application.add_handler(CommandHandler('update', update_data))
    # Run Aplikasi si Amicon
    application.add_handler(CommandHandler('start_amicon', start_amicon))
    

    #Message Handler harus d pasang paling terakhir
    application.add_handler(MessageHandler(filters.TEXT, read_command))
    application.add_handler(CallbackQueryHandler(button))

    # Run daily basis
    #j = application.job_queue.run_daily(kirim_laporan_jnmax,time=waktulaporanjnmax)
    k = application.job_queue.run_daily(update_realisasi_kemarin,time=waktuupdatekemarin)
    #l = application.job_queue.run_daily(update_spreadsheet_jnmax_uid,time=waktuupdatespreadsheetuid)
    m = application.job_queue.run_daily(update_realisasi_P2TL,time=waktuupdatep2tl)
    

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()
