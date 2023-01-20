from scraper import AP2T
from scraper import ACMT
from parameter import Parameter
from DataFrame import dataframe
import time


class Asmente():
    def buatCT(id_pelanggan: str, kodeunit: str, keteranganCT: str):
        # excute main
        print("Memulai New Asmen TE : ")
        pm = Parameter()
        df = dataframe()
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
                        id_pelanggan=id_pelanggan, petugas_dan_keterangan=keteranganCT, link_pengaduan_ct=link_pengaduan)
                    if (status == "yes" and int(nomoragenda) > 0):
                        print(message, "dengan nomor Agenda : ", nomoragenda)
                        # Get user untuk tindakan pengaduan, pake user spv TE
                        [link_tindakan_pengaduan_ct, username_ap2t, password_ap2t] = df.get_userlink_bykodeunit(
                            kdunit=kodeunit, jenis_user="TL TE", part_link_awal=pm.linktindakanpengaduan, part_link_akhir=pm.linktindakanpengaduan_2)
                        [status, message, nomoragenda] = ap2t.tindakan_pengaduan_ct(
                            nomor_agenda=nomoragenda, link_tindakan_pengaduan_ct=link_tindakan_pengaduan_ct)
                        if (status == "yes" and int(nomoragenda) > 0):
                            print(
                                "Berhasil Entry tindakan pengaduan dengan nomor agenda : ", nomoragenda)
                            [status, message, nomor_id] = ap2t.aktivasi_ct(
                                nomoragenda=nomoragenda, link_aktivasi_meter=pm.linkaktivasimeter)
                            print(message)
                            if (status == "yes" and int(nomor_id) > 0):
                                print("Eksekusi monitoring permohonan token")
                                status, message = ap2t.monitoring_token(
                                    tipe_pencarian=0, nomor_id=id_pelanggan, url_monitoring_token=pm.link_montok, url_cetak_token=pm.baselink_kct)
                                if (status == "yes"):
                                    print("Lanjut cetak Screenshoot")
                                    status, message = ap2t.take_screenshoot(
                                        direktori=pm.filepathct, file_name="fotoct.png")
                                    return "yes", message
                                else:
                                    message = "Gagal Eksekusi monitoring permohonan token"
                                    print(message)
                                    return "no", message
                            else:
                                print(message)
                                return "no", message
                    else:
                        print(message)
                        return "no", message

                else:
                    print(message)
                    return "no", message
            else:
                return "no", message
        else:
            print(message)
            return "no", message

    def cek_infopelanggan(tipe_pencarian: str, nomor_id: str, link_infopelanggan: str):
        pm = Parameter()
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        # Buka link info pelanggan
        [status, informasi, message] = ap2t.buka_info_pelanggan(
            tipe_pencarian=tipe_pencarian, nomor_id=nomor_id, link_infopelanggan=link_infopelanggan)
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
                return status, informasi, message
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
            message = "User tidak terdaftar\n" + "Message Error : "+str(e)
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
                "9615040FY", password_ap2t="Asdar-40")
            if (status == "yes"):
                print("Mencoba buka master imei")
                [status, message] = ap2t.buka_reset_imei(
                    nama_petugas=user_id, kode_unit=kode_unit)
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
