import pandas as pd


class Parameter:

    def __init__(self):

        # Setting server baru :
        # index, digunakan untuk server dengan spesifikasi rendah (os windows < 10)
        # 0 untuk server baru, 
        self.index = 0
        #1 untuk server lama uid
        #self.index = 1

        # nomortabdefault local dan server
        #nomortab local
        self.nomortabdefaultpengaduan = 1
        #nomortab server lama uid
        #self.nomortabdefaultpengaduan = 2
        # filepath executable file chromedriver, sesuaikan dengan versi chrome komputer masing2 server, jangan lupa di ekstrak
        self.filepathchromedriver = r'chromedriver\chromedriver.exe'
        # lokasi file executable AP2T Enkripsi, ada di folder PT PLN. AP2T Enkripsi
        self.filepathenkripsi = r'C:\Program Files (x86)\PT PLN (PERSERO)\AP2T ENKRIPSI\Token.exe'
        # jika mau menggunakan cache bawaan browser, silahkan di aktifkan (uncomment), lokasi atur sesuai lokasi cache
        #user option pc lokal
        #self.user_options = "user-data-dir=C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\User Data"
        self.user_options = "user-data-dir=C:\\Users\\CORE i7\\AppData\\Local\\Google\\Chrome\\User Data"
        #self.user_options = "user-data-dir=C:\\Users\\lenovo\\AppData\\Local\\Google\\Chrome\\User Data"
        #user option server lama uid
        #self.user_options = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
        # file list user
        self.filepathlistuser = r'data\listuser\listuser.xlsx'
        # sheet name list user
        self.sheetname_listuserid = "listuserid"
        self.fileexcelkct = r'krn\sudahbaca.xls'
        # filepath log
        self.filepathlog = r'data\log\log.xlsx'

        # pengaturan options security SSL
        self.ignore_ssl_errors = "--ignore-ssl-errors=yes"
        self.ignore_certificate_errors = "--ignore-certificate-errors"

        # setting bot baru
        # bot token id, di ganti jika ganti bot
        # self.tokenbot = "5686919975:AAH2BfsMAOsWrnbTbFCFAFcZsj8oADtMMtg"  # new_asmente_bot
        self.tokenbot = "5081663366:AAF9XrOVwtlD6gFTf7fh7qTbQXMixpe_XSI"  # ulpsgm_bot
        #self.tokenbot = "6811746544:AAFcvWpQhO65IDpKYRnQZFfujrkBEIkShHo"
        #self.tokenbot = "7389606593:AAGTPGLXb_AAzUalaaxDWo8Wwgq5DF1akXE" #Dalsutmsbot
        # group chat id
        self.chat_id = -828901164
        # chat_id admin
        # chat id luthfil, bisa di ganti disesuaikan dengan admin server
        self.chat_id_admin = 1029804860
        # self.chat_id_admin = 1150570046

        # Setting jika ada perubahan alamat, link atau domain dari aplikasi korporat
        # Link By Pass AP2T (Tidak usah di ubah jika tidak ada perubahan domain ap2t dari pusat)
        # Pengaduan CT
        self.linkpengaduanct = 'https://ap2t.pln.co.id/BillingTerpusatAP2TNew1-dr/redirect.jsp?user='
        self.linkpengaduanct_2 = '&page=tranI14&password=mblendez'
        self.linktindakanpengaduan = 'https://ap2t.pln.co.id/BillingTerpusatAP2TNew1-dr/redirect.jsp?user='
        self.linktindakanpengaduan_2 = '&page=tranI14Jwb&password=mblendez'
        self.linkaktivasimeter = "https://ap2t.pln.co.id/ap2t/frm_EntriMeter.aspx"
        self.link_montok = "https://ap2t.pln.co.id/BillingTerpusatAP2TNew1-dr/redirect.jsp?user=9009026F&password=mblendez&page=formMonitoringPermohonanToken"
        self.baselink_kct = "https://ap2t.pln.co.id/BillingTerpusatAP2TNew1-dr/ReportServlet?jenislaporan=getcetaktokenbynoagenda&report=report/CR_PK_TOKEN_LPB.pdf&noagenda="
        self.url_acmt = "https://portalapp.iconpln.co.id/acmt/"
        self.link_info_pelanggan = "https://ap2t.pln.co.id/infopelanggannewap2t-dr/"
        # reset imei
        self.url_resetimei = "https://ap2t.pln.co.id/acmt/Acmt.html?sessionid=4vfjje45dm11otflmo3wfrfn&page=frmMasterImei&userid=9615040FY"
        # link Update Realisasi TS
        self.url_tagsus1 = "https://ap2t.pln.co.id/BillingTerpusatAP2TNew1-dr/ReportServlet?jenislaporan=getlaporantsgab&report=report/NONREK/rpt_ts_daftar_realisasi_pendapatan_penetapan_ts.xls&unitup=SEMUA&unitap="
        self.kode_up3 = "32AMS"
        self.url_tagsus2 = "&unitupi="
        self.kode_uid = "32"
        self.url_tagsus3 = "&jenislap=DAFTAR%20REALISASI%20PENDAPATAN%20PENETAPAN%20TAGIHAN%20SUSULAN%20(TUNAI%20DAN%20ANGSURAN)&thbl="
        self.tahun_bulan = "202307"
        # Default (Di ganti sesuai kebutuhan developer/programmer)
        # Lokasi foto CT
        self.filepathct = 'fotoct\\'
        # lokasi download default
        self.files_foto_ct = 'fotoct\\fotoct.png'
        self.files_foto_kct = 'fotoct\\foto_kct.png'
        self.download_dir = 'data\\downloads'
        #lokasi download tagsus
        self.download_ts = 'data\\downloads'
        self.namafiletagsus = "ReportServlet.xls"
        self.link_spreadsheet_monitoringts = "https://docs.google.com/spreadsheets/d/1MNaFkKPb-RAmRvZZdMdVLK-AMPfG2PpMEysT8NnHEpg/edit#gid=1613659109"
        self.reporthariantab = "REPORT HARIAN TODAY"
        self.kiri_atas_layar_x = 57
        self.kiri_atas_layar_y = 279
        self.kanan_bawah_layar_x = 1855
        self.kanan_bawah_layar_y = 925
        # link ap2t
        self.urlap2t = 'https://ap2t.pln.co.id/ap2t/Login.aspx'
        self.filepathjson = R'data\gsheet\monitoringpju-290711-01d17333a9eb.json'
        self.filename_googlespreadsheet_tagsus = "Monitoring TS P2TL 2024"
        self.xpathreportharian =       "/html/body/div[4]/div/div[4]/table/tbody/tr[2]/td[3]/div/div[3]/div/div[3]"
        self.xpathreportharian_today = "/html/body/div[4]/div/div[4]/table/tbody/tr[2]/td[3]/div/div[3]/div/div[4]"
        
        # Parameter aplikasi si gadis
        #self.username_amicon = 'pusat\\firmansyah051'
        #self.password_amicon = '8206051F@30'
        self.username_amicon = 'pusat\\firmansyah051'
        self.password_amicon = '8206051F@36'
        self.bot_token = self.tokenbot
        self.user_browser_cache = "user-data-dir=C:\\Users\\CORE i7\\AppData\\Local\\Google\\Chrome\\User Data"
        #self.user_browser_cache = "user-data-dir=C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\User Data"

        #Parameter link foto rumah ACMT
        self.linkPart1_fotorumah = "https://portalapp.iconpln.co.id/acmt/DisplayBlobServlet7?idpel="
        self.linkPart2_fotorumah = "&blth="
        self.files_foto_rumah = 'fotoct\\fotorumah.jpg'
        self.files_foto_1 = 'fotoct\\foto1.jpg'
        self.files_foto_2 = 'fotoct\\foto2.jpg'
