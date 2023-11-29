from scraper import AP2T
from scraper import ACMT, Helper
from FILEMANAGER import filemanager
from parameter import Parameter
from DataFrame import dataframe
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import time
pm = Parameter()
df = dataframe()
# Import Amicon object
from scraper import Amicon


class Asmente():
    def buatCT(id_pelanggan: str, kodeunit: str, keteranganCT: str):
        # excute main
        print("Memulai New Asmen TE : ")
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        status = ap2t.open_ap2t()
        # Cek buka web ap2t
        if (status == "yes"):
            [link_pengaduan, username_ap2t,
                password_ap2t] = df.get_userlink_bykodeunit(kdunit=kodeunit, jenis_user="TL TEKNIK", part_link_awal=pm.linkpengaduanct, part_link_akhir=pm.linkpengaduanct_2)
            if (username_ap2t != "null" and password_ap2t != "0"):
                print("Login username : ")
                [status, message] = ap2t.login_ap2t(
                    username_ap2t=username_ap2t, password_ap2t=password_ap2t)
                # cek login
                if (status == "yes"):
                    print("Login Berhasil")
                    # Jika sukses, buat pengaduan
                    [status, message, nomoragenda] = ap2t.input_pengaduan_ct(
                        id_pelanggan=id_pelanggan, petugas_dan_keterangan=keteranganCT, link_pengaduan_ct=link_pengaduan, index=pm.index, nomortabdefault=1)
                    if (status == "yes" and int(nomoragenda) > 0):
                        print(message, "dengan nomor Agenda : ", nomoragenda)
                        # Get user untuk tindakan pengaduan, pake user spv TE
                        [link_tindakan_pengaduan_ct, username_ap2t, password_ap2t] = df.get_userlink_bykodeunit(
                            kdunit=kodeunit, jenis_user="TL TE", part_link_awal=pm.linktindakanpengaduan, part_link_akhir=pm.linktindakanpengaduan_2)
                        [status, message, nomoragenda] = ap2t.tindakan_pengaduan_ct(
                            nomor_agenda=nomoragenda, link_tindakan_pengaduan_ct=link_tindakan_pengaduan_ct, index=pm.index)
                        if (status == "yes" and int(nomoragenda) > 0):
                            print(
                                "Berhasil Entry tindakan pengaduan dengan nomor agenda : ", nomoragenda)
                            [status, message, nomor_id] = ap2t.aktivasi_ct(
                                nomoragenda=nomoragenda, link_aktivasi_meter=pm.linkaktivasimeter, index=pm.index)
                            print(message)
                            if (status == "yes" and int(nomor_id) > 0):
                                print("Eksekusi monitoring permohonan token")
                                status, jumlah_ct, message = ap2t.monitoring_token(
                                    tipe_pencarian=0, nomor_id=id_pelanggan, url_monitoring_token=pm.link_montok, url_cetak_token=pm.baselink_kct, index=pm.index)
                                if (status == "yes"):
                                    print("Lanjut cetak Screenshoot")
                                    status, message = ap2t.take_screenshoot(
                                        direktori=pm.filepathct, file_name="fotoct.png", index=pm.index)
                                    return "yes", jumlah_ct, message
                                else:
                                    message = "Gagal Eksekusi monitoring permohonan token"
                                    print(message)
                                    return "no", 0, message
                            else:
                                print(message)
                                return "no", 0, message
                    else:
                        print(message)
                        return "no", 0, message

                else:
                    print(message)
                    return "no", 0, message
            else:
                return "no", 0, message
        else:
            print(message)
            return "no", 0, message

    def cek_infopelanggan(tipe_pencarian: str, nomor_id: str, link_infopelanggan: str):
        pm = Parameter()
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        # Buka link info pelanggan
        [status, informasi, message] = ap2t.buka_info_pelanggan(
            tipe_pencarian=tipe_pencarian, nomor_id=nomor_id, link_infopelanggan=link_infopelanggan)
        return status, informasi, message

    def cek_pembelian_token(id_pelanggan : str):
        pm = Parameter()
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        [status, informasi, message] = ap2t.buka_history_token(id_pelanggan=id_pelanggan)
        return status, informasi, message
    def info_pelanggan_acmt(id_pelanggan: str):
        pm = Parameter()
        df = dataframe()
        acmt = ACMT(filepatchromedriver=pm.filepathchromedriver,
                    download_dir=pm.download_dir, user_options=pm.user_options, url_acmt=pm.url_acmt)
        status, message = acmt.open_acmt()
        if (status == "yes"):
            print(message)
            print("Memulai login ACMT")
            # get username and password
            [status_user, username_acmt, password_acmt] = df.get_user_acmt()
            [status, message] = acmt.login_acmt(username_acmt=username_acmt,
                                                password_acmt=password_acmt)
            if (status == "yes"):
                [status, informasi, message] = acmt.buka_informasi_pelanggan(
                    id_pelanggan)
                return status, informasi, message
            else:
                print(message)
                return status, "gagal get Info ACMT", message
        else:
            print(message)
            print("Gagal buka acmt")
            informasi = "null"
            return status, informasi, message

    def is_user_authenticated(chat_id: str):
        try:
            df = dataframe()
            pm = Parameter()
            [status, list_user, message] = df.get_authenticated_user(
                filepathlistuser=pm.filepathlistuser)
            print("Status : ", status, "\nMessage : ", message)
            print("List user id : ", chat_id)
            print("Tipe data chat id : ", type(chat_id))
            print(list_user)
            identifier = False
            for i in list_user:
                print(i, " Setelah konversi :", str(type(i)))
                print("list :", i, "Type : ", type(i))
                if (str(i) == str(chat_id)):
                    print("User di temukan")
                    message = "User terautentifikasi"
                    identifier = True
                    break
            print(message)
            if (identifier == True):
                return "yes", message
            else:
                message = "User tidak terdaftar, silahkan hubungi Admin"
                return "no", message

        except Exception as e:
            message = "Gagal mengecek id user\n" + "Message Error : "+str(e)
            return "no", message

    def kdunit_user(chat_id: int, kode_unit: int):
        df = dataframe()
        [status, kode_unit_user, message] = df.get_kode_unit_user(
            chat_id=chat_id)
        print("Memulai komparasi kode unit input dan hasil baca chat id user...")
        try:
            if (status == "yes" and str(kode_unit_user) == kode_unit):
                message = "Kode unit sesuai"
                print(message)
                return "yes", message
            else:
                message = "Tidak ada kode unit yang sesuai"
                print(message)
                return "no", message
        except Exception as e:
            message = "Kode unit tidak sesuai\nMessage Error : "+str(e)
            return "no", message

    def get_kode_unit(chat_id: int):
        dat = dataframe()
        [status, kode_unit, message] = dat.get_kode_unit_user(chat_id=chat_id)
        if (status == "yes"):
            return "yes", kode_unit, message
        else:
            return "no", kode_unit, message

    def get_level_user(chat_id: int):
        dat = dataframe()
        [status, level_user, message] = dat.get_level_user_data(
            chat_id=chat_id)
        if (status == "yes"):
            return "yes", level_user, message
        else:
            return "no", level_user, message

    def reset_imei(kode_unit: str, user_id: str):
        pm = Parameter()
        # buka AP2T
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver, filepathenkripsi=pm.filepathenkripsi,
                    urlap2t=pm.urlap2t, download_dir=pm.download_dir, filepathct=pm.filepathct, user_options=pm.user_options)
        status = ap2t.open_ap2t()
        if (status == "yes"):
            status, message = ap2t.login_ap2t(
                "9615040FY", password_ap2t="Asdar-41")
            if (status == "yes"):
                print("Mencoba buka master imei")
                [status, message] = ap2t.buka_reset_imei(
                    nama_petugas=user_id, kode_unit=kode_unit, index=pm.index)
                return "yes", message
            else:
                message = "Gagal Login AP2T, "+message
                return "no", message
        else:
            return "no", message

    def add_new_user(chat_id_daftar: int, kode_unit: int, nama: str, nomor_telfon: str, level: str):
        pm = Parameter()
        dat = dataframe()
        status, number_rows, message = dat.get_last_row(
            filepathlistuser=pm.filepathlistuser, sheetname="listuserid")
        if (status == "yes"):
            [status, message] = dat.write_data_userid(filepathlistuser=pm.filepathlistuser,
                                                      sheetname="listuserid", row=number_rows, kode_unit=kode_unit, nama=nama, nomor_telfon=nomor_telfon, level=level, chat_id=chat_id_daftar)
            if (status == "yes"):
                print(message)
                return "yes", message
            else:
                print(message)
                return "no", message
        else:
            print("Gagal get rows\n", message)
            return "no", message

    def get_kct_krn(Id_pelanggan: int):
        dat = dataframe()
        pm = Parameter()
        [status, message] = dat.baca_kct(
            filepath_kct_krn=pm.fileexcelkct, id_pelanggan=Id_pelanggan)
        return status, message

    def cek_blocking_token(id_pelanggan: str):
        pm = Parameter()
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver, filepathenkripsi=pm.filepathenkripsi,
                    urlap2t=pm.urlap2t, download_dir=pm.download_dir, filepathct=pm.filepathct, user_options=pm.user_options)
        status, message = ap2t.info_blocking_token(
            id_pelanggan=id_pelanggan)
        print(message)
        return status, message

    def info_montok(url_montok: str, tipe_pencarian: str, id_pencarian: str):
        pm = Parameter()
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        [status, message] = ap2t.buka_montok(url_montok=url_montok)
        if (status == "yes"):
            [status, message] = ap2t.get_history_montok(
                tipe_pencarian=tipe_pencarian, id_pencarian=id_pencarian)
            return "yes", message
        else:
            return "no", message

    def buatPengaduanHarAPP(id_pelanggan: str = "0", kode_unit: str = 0, nomor_meter_lama: str = 0, keterangan: str = "Tanpa Keterangan"):
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        # Login
        [link_pengaduan, username, password] = df.get_userlink_bykodeunit(
            kdunit=kode_unit, jenis_user="TL TEKNIK", part_link_awal=pm.linkpengaduanct, part_link_akhir=pm.linkpengaduanct_2)
        status = ap2t.open_ap2t()
        if (status == "yes"):
            [status, message] = ap2t.login_ap2t(
                username_ap2t=username, password_ap2t=password)
            if (status == "yes"):
                # Get link pengaduan
                [link_pengaduan, username, password] = df.get_userlink_bykodeunit(
                    kdunit=kode_unit, jenis_user="TL YAN GAN DAN ADM", part_link_awal=pm.linkpengaduanct, part_link_akhir=pm.linkpengaduanct_2)
                [status, message, nomoragenda] = ap2t.input_pengaduan_ct(
                    id_pelanggan=id_pelanggan, fungsi_dropdown="PENGADUAN TEKNIS", petugas_dan_keterangan=nomor_meter_lama+" Keterangan : "+keterangan, nomortabdefault=pm.nomortabdefaultpengaduan, link_pengaduan_ct=link_pengaduan)
                return "yes", message, nomoragenda
            else:
                return "no", message, 0
        else:
            return "no", message, 0

    def tindakanPengaduanHarAPP(nomoragenda: int, kode_unit: str):
        print("Memulai tindakan pengaduan Nomor Agenda : ", str(nomoragenda))
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        # Get user untuk tindakan pengaduan, pake user spv TE
        [link_tindakan_pengaduan_ct, username_ap2t, password_ap2t] = df.get_userlink_bykodeunit(
            kdunit=kode_unit, jenis_user="TL TE", part_link_awal=pm.linktindakanpengaduan, part_link_akhir=pm.linktindakanpengaduan_2)
        status, message, nomoragenda = ap2t.tindakan_pengaduan_ct(
            nomor_agenda=nomoragenda, link_tindakan_pengaduan_ct=link_tindakan_pengaduan_ct, nomortabdefault=pm.nomortabdefaultpengaduan, fungsi_dropdown="PENGADUAN TEKNIS")
        return status, message, nomoragenda

    def aktivasiHarAPP(nomoragenda: int, kode_unit: str, nomor_meter_baru: str):
        # print("Memulai aktivasi Har APP")
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        # Login
        [link_pengaduan, username, password] = df.get_userlink_bykodeunit(
            kdunit=kode_unit, jenis_user="TL TEKNIK", part_link_awal=pm.linkpengaduanct, part_link_akhir=pm.linkpengaduanct_2)
        status = ap2t.open_ap2t()
        if (status == "yes"):
            [status, message] = ap2t.login_ap2t(
                username_ap2t=username, password_ap2t=password)
            if (status == "yes"):
                # Get link Aktivasi meter
                [status, message, nomor_id] = ap2t.aktivasi_ct(
                    nomoragenda=nomoragenda, link_aktivasi_meter=pm.linkaktivasimeter, index=pm.index, nomortabdefault=pm.nomortabdefaultpengaduan, nomor_meter_baru=nomor_meter_baru, fungsi_dropdown="PENGADUAN TEKNIS")
                return "yes", message, nomoragenda
            else:
                message = "Gagal Aktivasi"
                return "no", message, 0
        else:
            message = "Gagal login"
            return "no", message, 0
    def create_lap_tsp2tl(kode_unit_user : str,tahun_bulan :str):
        #Hapus file report Servlet yang lama
        folder_path = pm.download_ts
        DF = dataframe()
        filename_and_extension = "ReportServlet.xls"
        [status,message] = filemanager.delete_file(folder_path=folder_path,filename_and_name_extension=filename_and_extension)
        if(status == "yes"):
            #jika berhasil hapus file, buka web Tagsus dan download file
            ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                        filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
            [status,message] = ap2t.buka_web_tagsus(kode_unit_user=kode_unit_user,tahun_bulan=tahun_bulan)
            if(status == "yes"):
                #baca data excel ReportServlet
                [status,message,df] = dataframe.read_reportservlet(skip_rows=8)
                #print(df)
                if(status == "yes"):
                    #tentukan nama tabnya sesuai bulannya
                    namatabbulan = dataframe.get_nama_sheet_bulan_sekarang()
                    #write data ke spreadsheet bulanan
                    TAB_NAME = namatabbulan #jangan lupa di variabelkan
                    [status,message] = dataframe.write_df_to_google_sheet(pm.filepathjson,GSHEET=pm.filename_googlespreadsheet_tagsus,TAB_NAME=TAB_NAME,df=df,first_row=9,first_col=1)
                    return "yes",message
                else:
                    return "no", message
            #kirim Laporan
            else:
                return "no",message
        else:
            return "no",message
    def kirim_report_ts():
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                        filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        #buka tabe REPORT HARIAN
        [status,message] = ap2t.buka_monitoring_ts(pm.link_spreadsheet_monitoringts,pm.reporthariantab)
        if(status == "yes"):
            #mengambil screenshoot
            #filemanager.take_screenshoot_pixel(kiri_atas_layar_x=pm.kiri_atas_layar_x,kiri_atas_layar_y=pm.kiri_atas_layar_y,kanan_bawah_layar_x=pm.kanan_bawah_layar_x,kanan_bawah_layar_y=pm.kanan_bawah_layar_y)
            message = "Berhasil kirim Report"
            print(message)
            return "yes",message
        else:
            return "no",message

    #acmt
    def get_foto_rumah(idpelanggan:str):
        acmt = ACMT(filepatchromedriver=pm.filepathchromedriver,
                    download_dir=pm.download_dir, user_options=pm.user_options, url_acmt=pm.url_acmt)
        status1,message = acmt.scraping_foto_1(idpelanggan=idpelanggan)
        status2,message = acmt.scraping_foto_2(idpelanggan=idpelanggan)
        statusrumah,message = acmt.scraping_foto_rumah(idpelanggan=idpelanggan)
        return status1,status2,statusrumah

    #AMICON
    def execute_amicon_not_login_state(idpel:str,amicon):
        amicon.login()
        #cek status menu comissioning
        status_menu_comiss = True
        counter = 0
        while status_menu_comiss:
            [status_menu_comiss,message] = amicon.click_comissioning()
            print(message)
            time.sleep(5)
            counter = counter+1
            if(counter > 15):
                break
        amicon.click_search_idpel_comissioning(idpel=idpel)
        #try click verify
        condition = True
        counter = 0
        while condition:
            condition = amicon.click_verify_test()
            time.sleep(5)
            counter = counter + 1
            if(counter > 50):
                break
        #klik pop up verify
        condition = True
        counter = 0
        while condition:
            condition = amicon.click_popup_verify()
            time.sleep(5)
            counter = counter + 1
            if(counter > 50):
                break
        #Confirm activate
        condition = True
        counter = 0
        while condition:
            condition = amicon.click_confirm_activate()
            time.sleep(5)
            counter = counter + 1
            if(counter > 50):
                break
        #Pop Up Confirm activate
        condition = True
        counter = 0
        while condition:
            condition = amicon.click_confirm_popup_activate()
            time.sleep(5)
            counter = counter + 1
            if(counter > 50):
                break
        #Proses Download PDF dan Finish Comissioning
        condition = True
        loop_value = 0
        while condition:
            try:
                print("Klik Download PDF")
                amicon.click_download_pdf_comissioning()
                condition = False
            except Exception as e:
                print("Gagal click Download PDF")
                time.sleep(5)
                condition = True
                loop_value = loop_value + 1
                if(loop_value > 50):
                    break

    def execute_amicon_login_state(idpel:str,amicon):
        #cek status menu comissioning
        status_menu_comiss = True
        counter = 0
        while status_menu_comiss:
            [status_menu_comiss,message] = amicon.click_comissioning()
            print(message)
            time.sleep(5)
            counter = counter+1
            if(counter > 15):
                break
        amicon.click_search_idpel_comissioning(idpel=idpel)
        #try click verify
        condition = True
        counter = 0
        while condition:
            condition = amicon.click_verify_test()
            time.sleep(5)
            counter = counter + 1
            if(counter > 50):
                break
        #klik pop up verify
        condition = True
        counter = 0
        while condition:
            condition = amicon.click_popup_verify()
            time.sleep(5)
            counter = counter + 1
            if(counter > 50):
                break
        #Confirm activate
        condition = True
        counter = 0
        while condition:
            condition = amicon.click_confirm_activate()
            time.sleep(5)
            counter = counter + 1
            if(counter > 50):
                break
        #Pop Up Confirm activate
        condition = True
        counter = 0
        while condition:
            condition = amicon.click_confirm_popup_activate()
            time.sleep(5)
            counter = counter + 1
            if(counter > 50):
                break
        #Proses Download PDF dan Finish Comissioning
        condition = True
        loop_value = 0
        while condition:
            try:
                print("Klik Download PDF")
                amicon.click_download_pdf_comissioning()
                condition = False
            except Exception as e:
                print("Gagal click Download PDF")
                time.sleep(5)
                condition = True
                loop_value = loop_value + 1
                if(loop_value > 50):
                    break

class ReplyButton():

    @staticmethod
    def opsi_aktivasi():
        buttons = [[InlineKeyboardButton("Pengaduan", callback_data="pengaduan")],
                   [InlineKeyboardButton("TindakanPengaduan", callback_data="tindakan")], [
            InlineKeyboardButton("Aktivasi", callback_data="aktivasiapp")],
            [InlineKeyboardButton("Cetak PK", callback_data="cetakpkaktivasi")], [InlineKeyboardButton(
                "Cetak BA", callback_data="cetakba")], [InlineKeyboardButton("cetakkct", callback_data="cetakkctaktivasi")],
            [InlineKeyboardButton("Peremajaan", callback_data="remaja")]]
        reply_markup = InlineKeyboardMarkup(buttons)
        return reply_markup

    def execute_button(data: str, kode_unit: int = "11111"):
        if (data == "pengaduan"):
            text_helper = "pengaduan|" + \
                str(kode_unit)+"|Idpel|NomorMeterLama|Keterangan dan petugas"
            return text_helper
        elif (data == "tindakan"):
            text_helper = "tindakanpengaduan|kode|18 Digit Nomor Agenda"
            return text_helper
        else:
            return "Kesalahan pada kode"
