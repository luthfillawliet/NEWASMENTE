from scraper import AP2T
from parameter import Parameter
import time


class Asmente():
    def buatCT(id_pelanggan):
        # excute main
        print("Memulai New Asmen TE : ")
        pm = Parameter()
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t, user_options=pm.user_options)
        status = ap2t.open_ap2t()
        # Cek buka web ap2t
        if (status == "yes"):
            status = ap2t.login_ap2t(
                username_ap2t="8208006F", password_ap2t="Des@2022")
            # cek login
            if (status == "yes"):
                print("Login Berhasil")
                # Jika sukses, buat pengaduan
                [status, message, nomoragenda] = ap2t.input_pengaduan_ct(
                    id_pelanggan=id_pelanggan, petugas_dan_keterangan="Luthfil Coba Bot CT", link_pengaduan_ct=pm.linkpengaduanct)
                if (status == "yes" and int(nomoragenda) > 0):
                    print(message, "dengan nomor Agenda : ", nomoragenda)
                    [status, message, nomoragenda] = ap2t.tindakan_pengaduan_ct(
                        nomor_agenda=nomoragenda, link_tindakan_pengaduan_ct=pm.linktindakanpengaduan)
                    if (status == "yes" and int(nomoragenda) > 0):
                        print(
                            "Berhasil Entry tindakan pengaduan dengan nomor agenda : ", nomoragenda)
                        [status, message, nomor_id] = ap2t.aktivasi_ct(
                            nomoragenda=nomoragenda, link_aktivasi_meter=pm.linkaktivasimeter)
                        print(message)
                        if (status == "yes" and int(nomor_id) > 0):
                            print("Eksekusi monitoring permohonan token")
                            ap2t.monitoring_token(
                                tipe_pencarian=0, nomor_id=id_pelanggan, url_monitoring_token=pm.link_montok, url_cetak_token=pm.baselink_kct)

                else:
                    print("Gagal input pengaduan")

            else:
                print("Gagal Login")
        else:
            print("Gagal buka Web AP2T")
