from parameter import Parameter

import time
import os
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pywinauto.application import Application


class AP2T:
    def __init__(self, filepathchromedriver, filepathenkripsi, urlap2t, download_dir, filepathct):

        self.filepathchromedriver = filepathchromedriver
        self.filepathenkripsi = filepathenkripsi
        self.urlap2t = urlap2t
        self.download_dir = download_dir
        self.filepathct = filepathct
        self.driver = webdriver.Chrome(filepathchromedriver)

    # Method buka AP2T
    def open_ap2t(self):
        print("Membuka halaman AP2T")
        driver = self.driver
        # Maximize page
        driver.maximize_window()
        # go to ap2t url
        try:
            driver.get(self.urlap2t)
            time.sleep(2)
            print("AP2T Berhasil di buka")
            return "yes"
        except:
            message = "Gagal membuka AP2T"
            print(message)
            return "no"

    def login_ap2t(self, username_ap2t, password_ap2t):
        try:
            # Masukkan UserID
            userid = WebDriverWait(driver=self.driver, timeout=2).until(
                EC.presence_of_element_located((By.ID, "tfUser"))
            )
            userid.send_keys(username_ap2t)
            # Masukkan Password
            passwordid = WebDriverWait(driver=self.driver, timeout=2).until(
                EC.presence_of_element_located((By.ID, "tfPassword"))
            )
            passwordid.send_keys(password_ap2t)
            # Buka Enkripsi
            app = Application().start(self.filepathenkripsi, timeout=10)
            # Print all controls on the dialog
            main_dlg = app.window(title='Informasi')
            main_dlg.print_control_identifiers()
            main_dlg.Button.click()
            time.sleep(2)
            main_dlg.type_keys("%{F4}")  # Alt-F4
            time.sleep(1)

            # paste enkripsi ke filed enkripsi
            enkripsi = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "lblEnkripsi"))
            )
            enkripsi.send_keys(Keys.CONTROL, "v")
            time.sleep(2)
            # klik tombol login
            try:
                btnLogin = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/form/div[7]/div[2]/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[2]/em/button"))
                )
                btnLogin.click()
                return "yes"
            except:
                message = "Gagal klk login"
                print(message)
                return "no"
        except:
            message = "Gagal login ap2t"
            print(message)
            return "no"

    def input_pengaduan_ct(self, idpelanggan, petugas_dan_keterangan, link_pengaduan_ct):
        try:
            # Buka Tab baru
            self.driver.execute_script(
                "window.open('https://ap2t.pln.co.id/BillingTerpusatAP2TNew1-dr/redirect.jsp?user=8609810Z&page=tranI14&password=mblendez');")
            time.sleep(5000)
            print("Berhasil buka tab ")
            # Pindah tab
            return "yes"

            # Buka Link Pengaduan Pelanggan CT
        except:
            message = "Gagal buka link pengaduan CT"
            print(message)
            return "no"
