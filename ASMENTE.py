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
                                message = "Gagal Aktivasi Token"
                                print(message)
                                return "no", message
                    else:
                        message = "Gagal input pengaduan"
                        print(message)
                        return "no", message

                else:
                    print(message)
                    return "no", message
            else:
                message = "Gagal membuat link dan ambil Username serta password"
                return "no", message
        else:
            message = "Gagal buka Web AP2T"
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
        acmt = ACMT(filepatchromedriver=pm.filepathchromedriver,
                    download_dir=pm.download_dir, user_options=pm.user_options, url_acmt=pm.url_acmt)
        status, message = acmt.open_acmt()
        if (status == "yes"):
            print(message)
            print("Memulai login ACMT")
            [status, message] = acmt.login_acmt(username_acmt=pm.username_acmt,
                                                password_acmt=pm.password_acmt)
            if (status == "yes"):
                [status, informasi, message] = acmt.buka_informasi_pelanggan()
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
