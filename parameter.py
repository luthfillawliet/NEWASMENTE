import pandas as pd


class Parameter:

    def __init__(self):
        # filepath executable file chromedriver, sesuaikan dengan versi chrome komputer masing2 server, jangan lupa di ekstrak
        self.filepathchromedriver = r'C:\xampp\htdocs\python\NEWASMENTE\chromedriver\chromedriver.exe'
        # lokasi file executable AP2T Enkripsi, ada di folder PT PLN. AP2T Enkripsi
        self.filepathenkripsi = r'C:\Program Files (x86)\PT PLN (PERSERO)\AP2T ENKRIPSI\Token.exe'
        # Lokasi foto CT
        self.filepathct = 'fotoct\\'
        # lokasi download default
        self.download_dir = 'download\\'
        # link ap2t
        self.urlap2t = 'https://ap2t.pln.co.id/ap2t/Login.aspx'

        self.filepathlistuser = r'\data\listuser\listuser.xlsx'

        # Link By Pass AP2T
        # Pengaduan CT
        self.linkpengaduanct = 'https://ap2t.pln.co.id/BillingTerpusatAP2TNew1-dr/redirect.jsp?user=8609810Z&page=tranI14&password=mblendez'
        self.linktindakanpengaduan = 'https://ap2t.pln.co.id/BillingTerpusatAP2TNew1-dr/redirect.jsp?user=8208006F&page=tranI14Jwb&password=mblendez'
