from scraper import AP2T
from parameter import Parameter
import time


class Asmente():
    def buatCT():
        # excute main
        print("Memulai New Asmen TE : ")
        pm = Parameter()
        ap2t = AP2T(filepathchromedriver=pm.filepathchromedriver,
                    filepathenkripsi=pm.filepathenkripsi, download_dir=pm.download_dir, filepathct=pm.filepathct, urlap2t=pm.urlap2t)
        status = ap2t.open_ap2t()
        # Cek buka web ap2t
        if (status == "yes"):
            status = ap2t.login_ap2t(
                username_ap2t="8208006F", password_ap2t="Des@2022")
            # cek login
            if (status == "yes"):
                print("Login Berhasil")
                ap2t.input_pengaduan_ct(
                    idpelanggan="321110070120", petugas_dan_keterangan="Luthfil Coba Bot CT", link_pengaduan_ct=pm.linkpengaduanct)
            else:
                print("Gagal Login")
        else:
            print("Gagal buka Web AP2T")
