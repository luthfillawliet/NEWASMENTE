from scraper import AP2T
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
                status = ap2t.login_ap2t(
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
                    message = "Gagal Login"
                    print(message)
                    return "no", message
            else:
                message = "Gagal membuat link dan ambil Username serta password"
                return "no", message
        else:
            message = "Gagal buka Web AP2T"
            print(message)
            return "no", message

    #  def infopelanggan(tipe_pencarian : str, nomor_id:str):
