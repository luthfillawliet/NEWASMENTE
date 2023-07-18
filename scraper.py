from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from pywinauto.application import Application
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# Library sigadis
import time
import pyautogui
import datetime
import os
import base64
import easyocr
from post_api import post_data

from DataFrame import dataframe
from parameter import Parameter
pm = Parameter()


class AP2T:
    def __init__(self, filepathchromedriver, filepathenkripsi, urlap2t, download_dir, filepathct, user_options):

        self.filepathchromedriver = filepathchromedriver
        self.filepathenkripsi = filepathenkripsi
        self.urlap2t = urlap2t
        self.download_dir = download_dir
        self.filepathct = filepathct
        self.download_dir_tagsus = pm.download_ts
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option('prefs',
        #                                        {"user-data-dir": "C:\\Users\\LENOVO\\AppData\\Local\\Google\\Chrome\\User Data"})
        chrome_options.add_argument(
            user_options)
        self.driver = webdriver.Chrome(
            executable_path=filepathchromedriver, options=chrome_options)

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
        except Exception as e:
            message = "Gagal membuka AP2T"
            print(message)
            print("Error message : ", e)
            return "no"

    def login_ap2t(self, username_ap2t: str, password_ap2t: str):
        print("USERNAME : ", username_ap2t, "PASSWORD : ", password_ap2t)
        try:
            # Masukkan UserID
            userid = WebDriverWait(driver=self.driver, timeout=2).until(
                EC.presence_of_element_located((By.ID, "tfUser"))
            )
            userid.clear()
            userid.send_keys(username_ap2t)
            # Masukkan Password
            passwordid = WebDriverWait(driver=self.driver, timeout=2).until(
                EC.presence_of_element_located((By.ID, "tfPassword"))
            )
            passwordid.clear()
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
                time.sleep(3)
                try:
                    welcome = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[1]/div[5]/div/div/div/div[1]/div/div[1]/div/table/tbody/tr/td[3]/span/span"))
                    )
                    message = "Berhasil Login"
                    return "yes", message
                except Exception as e:
                    message = "Gagal Login\nMessage Error : "+str(e)
                    print(message)
                    return "no", message
            except Exception as e:
                message = "Gagal klk login, pastikan user sedang tidak digunakan/Mac addres terdaftar\nError Message : " + \
                    str(e)
                print(message)
                return "no", message
        except Exception as e:
            message = "Gagal Entry username dan password\nError Message : " + \
                str(e)
            print(message)
            return "no", message

    def input_pengaduan_ct(self, id_pelanggan: str = "0", fungsi_dropdown: str = "PERMINTAAN CLEAR TAMPER", petugas_dan_keterangan: str = "", link_pengaduan_ct: str = "", index: int = 0, nomortabdefault: int = 1):
        try:
            print(link_pengaduan_ct)
            # Buka Tab baru
            self.driver.execute_script(
                "window.open('"+link_pengaduan_ct+"');")
            time.sleep(5)  # Bisa di ubah sesuai kebutuhan
            print("Berhasil buka tab permohonan pengaduan")
            try:
                # pindah tab ke tab pengaduan
                self.driver.switch_to.window(
                    self.driver.window_handles[nomortabdefault+index])
                # In
                tfidpel = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div/div/div/div[2]/div/div/div[2]/div/div/fieldset/div/div/div[1]/div[1]/input"))
                )
                tfidpel.send_keys(id_pelanggan)
                # tekan enter
                tfidpel.send_keys(Keys.RETURN)
                time.sleep(3)
                # Pilihan Dropdown
                dropdown = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div/div/div/div[1]/div/div/div[1]/div/div/fieldset/div/div/div[3]/div[1]/div/img"))
                )
                dropdown.click()
                time.sleep(1)
                # Get parent categories
                parentCategories = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_all_elements_located(
                        # (By.CLASS_NAME, "x-combo-list-inner")) #Berhasil untuk buat CT
                        (By.CLASS_NAME, "x-combo-list-item"))
                )
                try:
                    # print(str(len(child_elements)))
                    print("Berhasil get child elements")
                    print("jumlah item = ", str(len(parentCategories)))
                    for items in parentCategories:
                        print(items.text)
                        if (items.text.strip() == fungsi_dropdown):
                            print("Item ditemukan")
                            # klik itemnya
                            items.click()
                            break
                        else:
                            print("item tidak sesuai")
                    time.sleep(1)
                    # Input Petugas dan Keterangan
                    field_keterngan = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div/div/div/div[1]/div/div/div[2]/div/div/fieldset/div/div/div[4]/div[1]/textarea")
                        )
                    )
                    field_keterngan.send_keys(petugas_dan_keterangan)
                    time.sleep(1)  # Untuk troubleshoot saja
                    if (fungsi_dropdown == "PERMINTAAN CLEAR TAMPER"):
                        # pilih dropdown penyebab periksa
                        btnAlasan = WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div/div/div/div[1]/div/div/div[2]/div/div/fieldset/div/div/div[9]/div[1]/div/img"))
                        )
                        btnAlasan.click()
                        time.sleep(2)
                    try:
                        # get parent elements
                        parentPenyebab = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_all_elements_located(
                                (By.CLASS_NAME, "x-combo-list-item")
                            )
                        )
                        print(str(len(parentPenyebab)))
                        for items in parentPenyebab:
                            print(items.text)
                            print("Tipe data : ", type(items.text))
                            if (items.text.strip() == 'Muncul Informasi Call, Overload atau Lock'):
                                items.click()
                                print("berhasil pilih penyebab Periksa")
                                break
                            else:
                                print("Tidak ada Text yang sesuai")
                                # Keluar jika gagal menemukan penyebab pengaduan
                        # Save pengaduan
                        btnSave = WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div/div/div/div[1]/div/div/div[3]/div/div/fieldset/div/div[2]/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button"))
                        )
                        btnSave.click()
                        time.sleep(2)
                        # copy nomor agendanya
                        try:
                            noAgenda = WebDriverWait(self.driver, 15).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div/div/div/div[1]/div/div/div[1]/div/div/fieldset/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input"))
                            )
                            nomoragenda = noAgenda.get_attribute("value")
                            print(nomoragenda)
                            # klik tombol success nya
                            try:
                                btnSuccess = WebDriverWait(self.driver, 15).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "/html/body/div[14]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button"))
                                )
                                btnSuccess.click()
                                time.sleep(1)
                                return ["yes", "Berhasil buat pengaduan", nomoragenda]
                            except Exception as e:
                                message = "Gagal klik konfirmasi\nMessage Error : " + \
                                    str(e)
                                return ["yes", message, nomoragenda]
                        except Exception as e:
                            message = "Gagal get nomor agenda\nMessage Error : " + \
                                str(e)
                            return ["no", message, 0]
                    except:
                        message = "Gagal pilih dropdown penyebab"
                        print(message)
                        return ["no", message, 0]
                except Exception as e:
                    message = "Gagal pilih menu pengaduan\nMessage Error : " + \
                        str(e)
                    print(message)
                    return ["no", message, 0]
            except Exception as e:
                message = "Gagal input pengaduan\nError Message : "+str(e)
                print(message)
                return ["no", message, 0]
                # Buka Link Pengaduan Pelanggan CT
        except:
            message = "Gagal buka link pengaduan CT"
            print(message)
            return ["no", message, 0]

    def tindakan_pengaduan_ct(self, nomor_agenda, link_tindakan_pengaduan_ct, fungsi_dropdown: str = "PERMINTAAN CLEAR TAMPER", index: int = 0, nomortabdefault: int = 2, uraian_tindakan: str = "GANTI KWH METER", alasan_ganti_meter: str = "Relay rusak"):
        try:
            # Buka Tab baru
            self.driver.execute_script(
                "window.open('"+link_tindakan_pengaduan_ct+"');")
            time.sleep(5)  # Bisa di ubah sesuai kebutuhan
            try:
                # pindah tab ke tab pengaduan
                self.driver.switch_to.window(
                    self.driver.window_handles[nomortabdefault+index])
                print("Berhasil buka tab Tindakan pengaduan")
                # Clsoe pop up  notif
                btnClose = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[6]/div[1]/div/div/div/div"))
                )
                btnClose.click()
                print("Berhasil close pop up")
                time.sleep(1)
                # entry nomor agenda
                field_noagenda = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div/div/div/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input"))
                )
                field_noagenda.send_keys(nomor_agenda)
                time.sleep(.5)
                field_noagenda.send_keys(Keys.RETURN)
                time.sleep(3)
                # Jika fungsi permintaan clear tamper
                if (fungsi_dropdown == "PERMINTAAN CLEAR TAMPER"):
                    # save nomor agenda
                    try:
                        btnSaveT = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "/html/body/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div/div/div/div[2]/div[1]/div/div/div/form/fieldset[4]/div/div[2]/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button"))
                        )
                        btnSaveT.click()
                        time.sleep(1)
                        message = "Berhasil menyimpan tindakan pengaduan"
                        print(message)
                        return ["yes", message, nomor_agenda]
                    except Exception as e:
                        message = "Gagal klik btn Save\nMessage Error : " + \
                            str(e)
                        return "no", message, 0
                elif (fungsi_dropdown == "PENGADUAN TEKNIS"):
                    # Klik dropdown Uraian tindakan
                    dropdown_btn = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div/div/div/div[2]/div[1]/div/div/div/form/fieldset[2]/div/div/div[3]/div[1]/div/img"))
                    )
                    dropdown_btn.click()
                    parentCategories = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_all_elements_located(
                            # (By.CLASS_NAME, "x-combo-list-inner")) #Berhasil untuk buat CT
                            (By.CLASS_NAME, "x-combo-list-item"))
                    )
                    try:
                        # print(str(len(child_elements)))
                        print("Berhasil get child elements")
                        print("jumlah item = ", str(len(parentCategories)))
                        for items in parentCategories:
                            print(items.text)
                            # Di sesuaikan alasan ganti meternya
                            if (items.text.strip() == uraian_tindakan):
                                print("Item ditemukan")
                                # klik itemnya
                                items.click()
                                break
                            else:
                                print("item tidak sesuai")
                        time.sleep(1)
                        # search Alasan Ganti Meter
                        try:
                            dropdown_btn_alasan = WebDriverWait(self.driver, 15).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "/html/body/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div/div/div/div[2]/div[1]/div/div/div/form/fieldset[2]/div/div/div[6]/div[1]/div/img"))
                            )
                            dropdown_btn_alasan.click()
                            # Pilih alasan ganti meter
                            parentCategories = WebDriverWait(self.driver, 15).until(
                                EC.presence_of_all_elements_located(
                                    (By.CLASS_NAME, "x-combo-list-item"))
                            )
                            for items in parentCategories:
                                print(items.text)
                                # Di sesuaikan alasan ganti meternya
                                if (items.text.strip() == alasan_ganti_meter):
                                    print("Item ditemukan")
                                    # klik itemnya
                                    items.click()
                                    break
                                else:
                                    print("item tidak sesuai")
                            # save nomor agenda
                            try:
                                btnSaveT = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "/html/body/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div/div/div/div[2]/div[1]/div/div/div/form/fieldset[4]/div/div[2]/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button"))
                                )
                                btnSaveT.click()
                                time.sleep(1)
                                message = "Berhasil menyimpan tindakan pengaduan"
                                print(message)
                                time.sleep(1)
                                return ["yes", message, nomor_agenda]
                            except Exception as e:
                                message = "Gagal klik btn Save\nMessage Error : " + \
                                    str(e)
                                return "no", message, 0
                        except Exception as e:
                            message = "Gagal pilih Alasan ganti meter\nMessage Error : " + \
                                str(e)
                            return ["no", message, 0]
                    except Exception as e:
                        message = "Gagal pilih uraian tindakan\nMessage Error : " + \
                            str(e)
                        print(message)
                        return ["no", message, 0]
            except Exception as e:
                message = "Gagal entry tindakan pengaduan\nMessage Error : " + \
                    str(e)
                print(message)
                return ["no", message, 0]
        except Exception as e:
            message = "Gagal Buka Halaman Tindakan pengaduan\nMessage Error : " + \
                str(e)
            print(message)
            return ["no", message, 0]

    def aktivasi_ct(self, nomoragenda, link_aktivasi_meter, index: int = 0, nomortabdefault: int = 3, nomor_meter_baru: int = 0, fungsi_dropdown: str = "PERMINTAAN CLEAR TAMPER"):
        try:
            print("Memulai aktivasi token")
            self.driver.execute_script(
                "window.open('"+link_aktivasi_meter+"');")
            time.sleep(5)  # Bisa di ubah sesuai kebutuhan
            # pindah tab ke tab pengaduan
            self.driver.switch_to.window(
                self.driver.window_handles[nomortabdefault+index])
            noAgendaAktivasi = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/form/div[3]/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div/div[1]/fieldset/div/div/div/div[1]/div/div[2]/input"))
            )
            noAgendaAktivasi.send_keys(nomoragenda)
            time.sleep(.5)
            # klik cari
            btnCari = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/form/div[3]/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div/div[1]/fieldset/div/div/div/div[1]/div/div[3]/table/tbody/tr/td[2]/em/button"))
            )
            btnCari.click()
            time.sleep(3)
            if (fungsi_dropdown == "PERMINTAAN CLEAR TAMPER"):
                # klik simpan
                btnSimpan = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/form/div[3]/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td[2]/em/button"))
                )
                btnSimpan.click()
                # confirm simpan
                btnSimpan = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td[2]/table"))
                )
                btnSimpan.click()
                time.sleep(1)
                message = "Berhasil aktivasi token"
                return ["yes", message, nomoragenda]
            elif (fungsi_dropdown == "PENGADUAN TEKNIS"):
                print("Fungsi dropdown yang di eksekusi :  "+fungsi_dropdown)
                # Masukkan nomor kWh meter baru
                text_field = WebDriverWait(self.driver, 10).until(
                    # EC.presence_of_element_located(
                    # (By.XPATH, "/html/body/form/div[3]/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div/div[3]/fieldset/div/div/div[1]/div[1]/div/input[2]"))
                    EC.presence_of_element_located((By.ID, "cNoMeter"))
                )
                text_field.send_keys(nomor_meter_baru)
                text_field.send_keys(Keys.RETURN)
                time.sleep(2)
                print(text_field.get_attribute("value"))
                try:
                    # save
                    btnSimpan = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/form/div[3]/div/div/div/div/div/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td[2]/em/button"))
                        # (By.CLASS_NAME, "x-btn-text icon-databasesave"))
                    )
                    btnSimpan.click()
                    print("Berhasil klik pertama")
                    time.sleep(3)
                    # notif nomor meter kosong muncul
                    try:
                        btnClose = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "/html/body/div[6]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/table"))
                        )
                        btnClose.click()
                        time.sleep(1)
                        btnSimpan.click()
                        time.sleep(3)
                        # Tekan tombol konfirmasi
                        try:
                            print("Coba klik ya")
                            time.sleep(5)  # DI hapus nanti
                            parentCategories = WebDriverWait(self.driver, 15).until(
                                EC.presence_of_all_elements_located(
                                    # (By.CLASS_NAME, "x-combo-list-inner")) #Berhasil untuk buat CT
                                    (By.CLASS_NAME, "x-panel-btn-td"))
                            )
                            try:
                                # print(str(len(child_elements)))
                                print("Berhasil get child elements")
                                print("jumlah item = ", str(
                                    len(parentCategories)))
                                for items in parentCategories:
                                    print(items.text)
                                    if (items.text.strip() == "Ya"):
                                        print("Item ditemukan")
                                        # klik itemnya
                                        items.click()
                                        break
                                    else:
                                        print("item tidak sesuai")
                                time.sleep(1)
                                return ["yes", message, nomoragenda]
                            except Exception as e:
                                message = "Gagal klik tombol konfirmasi\nMessage Error : " + \
                                    str(e)
                                return ["no", message, 0]
                        except Exception as e:
                            message = "Gagal klik tombol konfirmasi\nMessage Error : " + \
                                str(e)
                            return ["no", message, 0]
                    except Exception as e:
                        message = "Notif error nomor metr tidak muncul\nMessage Error : " + \
                            str(e)
                        return ["no", message, 0]
                except Exception as e:
                    message = "Gagal klik simpan\nMessage Error : "+str(e)
                    print("gagal klik simpan")
                    return "no", message, 0
        except:
            message = "Gagal aktivasi token"
            print(message)
            return ["no", message, nomoragenda]

    def monitoring_token(self, tipe_pencarian, nomor_id, url_monitoring_token, url_cetak_token, index: int = 0):
        # Buka link monitoring token

        # Tipe pencarian : 0, jika idpel, 1 jika nomor meter. dan 2 jika nomor agenda
        if (tipe_pencarian == 0):
            # Eksekusi pencarian berdasarkan Idpel
            print("Cari token berdasarkan Idpel")
            self.monitoring_cari_idpel(
                url_montok=url_monitoring_token, idpel=nomor_id, index=index)
            status, jumlahCT = self.get_jumlah_request(
                jenis_token="CLEAR TAMPER")
            nomoragenda = self.show_last_kct()
            if (nomoragenda != "0"):
                self.cetak_token(nomoragenda=nomoragenda,
                                 link_ct=url_cetak_token)
                return ["yes", jumlahCT, "Cari token berdasarkan Idpel Berhasil"]
            else:
                return ["no", 0, "Gagal cari token berdasarkan idpel"]
        elif (tipe_pencarian == 2):
            # Eksekusi pencarian berdasarkan Nomor Meter
            print("Cari token berdasarkan Nomor Meter")
        elif (tipe_pencarian == 3):
            # Eksekusi pencarian berdasarkan Nomor Agenda
            print("Cari token berdasarkan Nomor Agenda")
        else:
            # Kode dasar pencarian tidak dikenal
            print("Kode dasar pencarian tidak dikenal")

    def monitoring_cari_idpel(self, url_montok, idpel, index: int = 0):
        try:
            # masukkan idpel
            self.driver.execute_script(
                "window.open('"+url_montok+"');")
            time.sleep(5)  # Bisa di ubah sesuai kebutuhan
            # pindah tab ke tab pengaduan
            # Ubah untuk testing dan run
            self.driver.switch_to.window(self.driver.window_handles[4+index])
            # klik dropdown kategori search
            btnKategori = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/form/table/tbody/tr[3]/td/fieldset/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/img"))
            )
            btnKategori.click()
            print("Berhasil klik")
            time.sleep(1)
            # get semua child element dulu
            parentCategories = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "x-combo-list-item"))
            )
            print("Panjang Array : "+str(len(parentCategories)))
            print(str(len(parentCategories)))
            for items in parentCategories:
                if (items.text == "PER IDPEL"):
                    items.click()
                    break
            print("Berhasil klik pilihan dropdown")
            tfIdpel = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/form/table/tbody/tr[3]/td/fieldset/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input"))
            )
            tfIdpel.send_keys(idpel)
            print("Entry Idpel berhasil")
            btnFilter = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/form/table/tbody/tr[4]/td/div/div/div[2]/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]"))
            )
            # Klik search idpel
            btnFilter.click()
            print("Berhasil klik Filter")
            time.sleep(1)
            message = "Berhasil Ambil monitoring token"
            return ["yes", message]
        except:
            message = "Gagal cari monitoring token berdasarkan IDPEL"
            return ["no", message]

    def get_jumlah_request(self, jenis_token):
        print("Menghitung request token")
        # Get jumlah permintaan CT
        try:
            kctrows = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "x-grid3-row"))
            )
            # kctrows_childs = kctrows.find_elements_by_class_name(
            #     "x-grid3-row")
            print("panjang rows : "+str(len(kctrows)))
            jumlah_token = 0
            for i in range(len(kctrows)):
                print("membaca rows ke : ", str(i))
                iteration_nth = "/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/form/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(
                    i+1)+"]/table/tbody/tr/td[10]/div"
                col_value = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(
                        (By.XPATH, iteration_nth)
                    )
                )
                print(col_value.text)
                if (col_value.text.strip() == jenis_token):
                    jumlah_token = jumlah_token+1
                    print("Sama")
                else:
                    pass
            message = ("Jumlah Permintaan " + jenis_token +
                       "adalah :" + str(jumlah_token))
            print(message)

            return message, jumlah_token
        except Exception as e:
            message = "Gagal hitung jumlah token"
            print(message)
            print(e)
            return ["no", 0]

    def show_last_kct(self):
        try:
            print("Cek status token ...")
            xpath_status = "/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/form/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[14]/div"
            status_token = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, xpath_status))
            )
            btnfilter = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/form/table/tbody/tr[4]/td/div/div/div[2]/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]")))

            while status_token.text.strip() != "SUKSES TOKEN":
                time.sleep(3)
                btnfilter.click()
                time.sleep(2)
                # Cek status lagi
                status_token = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, xpath_status))
                )
                if (status_token.text.strip() == "SUKSES TOKEN"):
                    print("Berhasil ubah status token")
                    break
                else:
                    print("Status token : ", status_token.text)
            # Get nomor agenda jika sudah sukses
            nomoragenda = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/form/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[1]/div")))
            print("Sukses cetak token no agenda : ",
                  nomoragenda.text, status_token.text)
            return nomoragenda.text
        except Exception as e:
            message = "Gagal ambil status token dan nomor agenda"
            print(message)
            print("Error Message : ", e)
            return "0"

    def cetak_token(self, nomoragenda, link_ct):
        try:
            print("Memulai Cetak token")
            # merge link dengan nomor agenda
            link_ct = link_ct+nomoragenda
            # Buka tab baru
            self.driver.execute_script(
                "window.open('"+link_ct+"');")
            time.sleep(5)  # Bisa di ubah sesuai kebutuhan
            message = "Berhasil cetak token"
            return ["yes", message]
        except Exception as e:
            return ["no"]

    def take_screenshoot(self, direktori: str, file_name: str, numbertab: int = 5, index: int = 0):
        print("Memulai screenshoot")
        time.sleep(3)
        # ganti jika tes dan running
        self.driver.switch_to.window(
            self.driver.window_handles[numbertab+index])
        try:
            self.driver.save_screenshot(direktori+"fotoct.png")
            message = "Berhasil kirim screenshot"
            return "yes", message
        except Exception as e:
            message = "Gagal screenshot"
            print("Error Message : ",  e)
            return "yes", message

    def buka_info_pelanggan(self, tipe_pencarian: str, nomor_id: str, link_infopelanggan: str):
        print("Membuka halaman Info Pelanggan")
        print("Tipe Pencarian yang di gunakan : ", tipe_pencarian)
        driver = self.driver
        # Maximize page
        driver.maximize_window()
        # go to ap2t url
        try:
            driver.get(link_infopelanggan)
            time.sleep(2)
            print("Info Pelanggan Berhasil di buka")
            # find edit text input
            edit_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/fieldset/div/div/div[4]/div/div/div/div[2]/div/div/div/div[1]/input"))
            )
            edit_text.send_keys(nomor_id)
            # pilih kategori
            dropdwon_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/fieldset/div/div/div[4]/div/div/div/div[1]/div/div/div/div[1]/div/img"))
            )
            dropdwon_btn.click()
            time.sleep(1)
            # pilih metode pencarian
            categories = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "x-combo-list-item"))
            )
            print("Jumlah Kategori : ", str(len(categories)))
            # Looping untuk get access tiap value dari kategori
            try:
                for i in categories:
                    print(i.text)
                    if (i.text.strip() == tipe_pencarian):
                        i.click()
                        break
                    else:
                        print("Kategori tidak ditemukan")
                # Loading load data
                time.sleep(1)
                btnSearch = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button"))
                )
                btnSearch.click()
                time.sleep(3)
                # Ekstract Id Pelanggan
                element0 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div/table/tbody/tr/td[1]/div"))
                )
                id_pelanggan = element0.text
                id_pelanggan = "Id Pelanggan : "+id_pelanggan+"\n"
                print(id_pelanggan)
                # Klik Tab DIL,sub tab main
                btnDil = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[1]/div[1]/ul/li[2]"))
                )
                btnDil.click()
                # Ekstract Info pelanggan
                element1 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input"))
                )
                namapelanggan = element1.get_attribute("value")
                namapelanggan = "Nama Pelanggan : "+namapelanggan+"\n"
                element2 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/input"))
                )
                tarif = element2.get_attribute("value")
                tarif = "Tarif : "+tarif+"\n"
                element3 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/input"))
                )
                daya = element3.get_attribute("value")
                daya = "Daya : "+daya+"\n"
                time.sleep(1)
                # PNJ
                element4 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[5]/div/div/div/div[1]/div/div/div/div[1]/input"))
                )
                # Nama PNJ
                element5 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[5]/div/div/div/div[2]/div/div/div/div[1]/input"))
                )
                # No Bang
                element6 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[5]/div/div/div/div[3]/div/div/div/div[1]/input"))
                )
                # Ket No bang
                element7 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[5]/div/div/div/div[4]/div/div/div/div[1]/input"))
                )
                # Kabupaten
                element8 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div/div/div[2]/div/div/div/div[1]/input"))
                )
                # Kecamatan
                element9 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div/div/div[3]/div/div/div/div[1]/input"))
                )
                # Desa
                element10 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div/div/div[4]/div/div/div/div[1]/input"))
                )
                alamat = "Alamat : "+element4.get_attribute("value") + " "+element5.get_attribute("value")+" "+element6.get_attribute("value")+" "+element7.get_attribute(
                    "value")+" ,"+element10.get_attribute("value")+" ,"+element9.get_attribute("value")+" ,"+element8.get_attribute("value")+"\n"
                # Klik tab APP
                tabApp = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/ul/li[4]"))
                )
                tabApp.click()
                # tab APP
                # Get Nomor Meter
                element11 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/input"))
                )
                nomor_meter = element11.get_attribute("value")
                nomor_meter = "Nomor kWh Meter : "+nomor_meter+"\n"
                print(nomor_meter)
                # Get Merk kWh Meter
                element12 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input"))
                )
                merk_meter = element12.get_attribute("value")
                merk_meter = "Merk kWh Meter : "+merk_meter+"\n"
                print(merk_meter)
                versiKRN = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[4]/div/div/div/div[1]/div/div/div/div[1]/input"))
                )
                krn = "Versi KRN : "+versiKRN.get_attribute("value")+"\n"
                # Get Faktor Kali Meter
                element13 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div/div/div/div[6]/div/div/div/div[1]/input"))
                )
                fkm = element13.get_attribute("value")
                fkm = "Faktor Kali Meter : "+fkm+"\n"
                # Merge semua data
                dataPelanggan = id_pelanggan+nomor_meter + \
                    namapelanggan+tarif+daya+alamat+merk_meter+krn+fkm
                time.sleep(1)
                informasi = dataPelanggan
                message = "Berhasil Ambil Info Pelanggan"
                time.sleep(1)
                return "yes", informasi, message
            except Exception as e:
                message = "Kategori gagal di peroleh\nMessage Error : "+str(e)
                print(message)
                return "no", "null", message
        except Exception as e:
            message = "Gagal membuka Info Pelanggan"
            print(message)
            print("Error message : ", e)
            return "no", "null", message

    def just_buka_info_pelanggan(self):
        pm = Parameter()
        print("Membuka halaman Info Pelanggan")
        # go to ap2t url
        try:
            self.driver.get(pm.link_info_pelanggan)
            time.sleep(2)
            message = "Info Pelanggan Berhasil di buka"
            print(message)
            return "yes", message
        except Exception as e:
            message = "Gagal membuka Info Pelanggan\nMessage Error : "+str(e)
            print(message)
            print("Error message : ", e)
            return "no", message

    def buka_reset_imei(self, nama_petugas: str, kode_unit: str, index: int = 0):
        try:
            # Menu pencatatan meter
            menu_imei = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[5]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/ul/li/ul/li[2]/div"))
            )
            # double click
            action = ActionChains(self.driver)
            action.double_click(menu_imei).perform()
            time.sleep(1)
            # Catat meter terpusat
            menu_imei = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[5]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/ul/li/ul/li[2]/ul/li[8]/div"))
            )
            action.double_click(menu_imei).perform()
            time.sleep(1)
            # Master imei
            menu_imei = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[5]/div/div/div/div[2]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/ul/li/ul/li[2]/ul/li[8]/ul/li[4]/div"))
            )
            menu_imei.click()
            time.sleep(2)
            try:
                # identifikasi div IMEI
                div_imei = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.ID, "Master Imei_IFrame"))
                )
                print("Berhasil identifikasi tab reset imei")
                src_value = div_imei.get_attribute("src")
                print("Src: ", src_value)
                # klik dropdown
                try:
                    # buka di new tab
                    # Buka Tab baru
                    self.driver.execute_script(
                        "window.open('"+src_value+"');")
                    time.sleep(3)  # Bisa di ubah sesuai kebutuhan
                    # pindah di tab baru
                    self.driver.switch_to.window(
                        self.driver.window_handles[1+index])
                    print("Berhasil PINDAH KE TAB BARU RESET IMEI")
                    # get child element
                    btn_dropdown = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[3]/div/div[2]/div"))
                    )
                    btn_dropdown.click()
                    print("Berhasil klik dropdown")
                    time.sleep(1)
                    # hitung jumlah klik
                    df = dataframe()
                    jumlahklik = df.get_jumlah_klik_resetimei(
                        kodeunit_cari=int(kode_unit))
                    print("Jumlah klik :", jumlahklik)
                    pyautogui.press('down', presses=jumlahklik)
                    # JANGAN LUPA JADIKAN PARAMETER
                    print("berhasil klik down 3x")
                    time.sleep(1)
                    pyautogui.press('return')
                    time.sleep(1)
                    btn_load = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[5]/div/table/tbody/tr[2]/td[2]/em/button"))
                    )
                    btn_load.click()
                    time.sleep(1)
                    # hitung jumlah row petugas
                    ptgs_rows = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, "x-grid3-row"))
                    )
                    print("JUmlah petugas : ", str(len(ptgs_rows)))
                    print("Nama petugas pencarian = "+nama_petugas)
                    for i in range(len(ptgs_rows)):
                        xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div["+str(
                            i+1)+"]/table/tbody/tr/td[2]"
                        selected_rows = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, xpath))
                        )
                        print("nama petugas row : "+str(i+1) +
                              " = "+selected_rows.text)
                        # JANGAN LUPA DI VARIABELKAN
                        if (selected_rows.text.strip() == (kode_unit+"."+nama_petugas)):
                            print("petugas ditemukan")
                            selected_rows.click()
                            print("petugas di klik")
                            time.sleep(1)
                            break
                        else:
                            print("petugas tidak ditemukan")
                    # Klik tombolnya
                    btn_reset = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/div/form/div/div[2]/div[2]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button"))
                    )
                    btn_reset.click()
                    time.sleep(1)
                    # yes
                    btn_reset = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[6]/div[2]/div[2]/div/div/div/div/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/em/button"))
                    )
                    btn_reset.click()
                    time.sleep(5)
                    return "yes", "Berhasil reset imei user"
                except Exception as e:
                    message = "Gagal find unit\nMessage Error : "+str(e)
                    print(message)
                    return "no", message
            except Exception as e:
                message = "Gagal identifikasi tab reset imei\nMessage Error : " + \
                    str(e)
                print(message)
        except Exception as e:
            print("Gagal klik dropdown\nMessage Error : "+str(e))

    def info_blocking_token(self, id_pelanggan: str):
        self.driver.maximize_window()
        [status, message] = self.just_buka_info_pelanggan()
        print(message)
        if (status == "yes"):
            time.sleep(1)
            # masukkan idpel
            # # find edit text input
            edit_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/fieldset/div/div/div[4]/div/div/div/div[2]/div/div/div/div[1]/input"))
            )
            edit_text.send_keys(id_pelanggan)
            # pilih kategori
            dropdwon_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/fieldset/div/div/div[4]/div/div/div/div[1]/div/div/div/div[1]/div/img"))
            )
            dropdwon_btn.click()
            time.sleep(1)
            # pilih metode pencarian
            categories = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "x-combo-list-item"))
            )
            print("Jumlah Kategori : ", str(len(categories)))
            # Looping untuk get access tiap value dari kategori
            try:
                for i in categories:
                    print(i.text)
                    if (i.text.strip() == "Id Pelanggan"):
                        i.click()
                        break
                    else:
                        print("Kategori tidak ditemukan")
                # Loading load data
                time.sleep(1)
                btnSearch = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button"))
                )
                btnSearch.click()
                time.sleep(2)
                ############################# TARUH FUNGSI YANG MAU DI LAKUKAN DI SINI ###############################
                try:
                    # buka tab info prepaid
                    tabPrepaid = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[1]/div[1]/ul/li[8]"))
                    )
                    tabPrepaid.click()
                    print("Berhasil kli tab prepaid")
                    time.sleep(1)
                    tabPrepaid = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/table/tbody/tr/td/div/div/div/div/div[1]/div[1]/ul/li[6]"))
                    )
                    tabPrepaid.click()
                    time.sleep(1)
                    # Get jumlah rows blocking token
                    try:
                        rows_got = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, "x-grid3-row-table")))
                        print("JUmlah rows : ", str(len(rows_got)))
                        message = "Nomor Register Tunggakan Idpel "+id_pelanggan+" :\n"
                        time.sleep(1)

                        # jumlah_tunggakan = len(child_elements)
                        # print("Jumlah tunggakan = "+str(jumlah_tunggakan))
                        # inforegister = ""
                        if (len(rows_got)) > 0:
                            for i in range(len(rows_got)):
                                print("\nTunggakan ke - "+str(i+1))
                                try:
                                    cell_nomor_register = WebDriverWait(self.driver, 2).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH, ("/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/table/tbody/tr/td/div/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(i+1)+"]/table/tbody/tr/td[3]/div")))
                                    )
                                    cell_rupiah = WebDriverWait(self.driver, 3).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH, ("/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/table/tbody/tr/td/div/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(i+1)+"]/table/tbody/tr/td[6]/div")))
                                    )
                                    tgl_jth_tempo = WebDriverWait(self.driver, 3).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH, ("/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div[2]/div/div[2]/div/div/table/tbody/tr/td/div/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(i+1)+"]/table/tbody/tr/td[4]/div")))
                                    )
                                    # tanggal jatuh tempo
                                    print("Nomor Register : " +
                                          cell_nomor_register.text + " Rupiah Tag : "+cell_rupiah.text)
                                    message = message+"No register : "+cell_nomor_register.text + \
                                        " Rupiah Tag : "+cell_rupiah.text+" Jatuh tempo : "+tgl_jth_tempo.text+"\n"
                                except Exception:
                                    pass
                            print(message)
                            return "yes", message
                        else:
                            message = "Nomor register tidak ada"
                            return "yes", message
                    except Exception as e:
                        message = "Gagal hitung jumlah rows"
                        print(message)
                        return "no", message
                except Exception as e:
                    message = "Gagal cek tab blocking token\nMessage Error : " + \
                        str(e)
                    return "no", message
            except Exception as e:
                message = "Kategori gagal di peroleh\nMessage Error : "+str(e)
                print(message)
                return "no", message

    def buka_montok(self, url_montok: str):
        try:
            self.driver.get(url_montok)
            message = "berhasil buka monitoring permohonan token"
            return "yes", message
        except Exception as e:
            message = "Gagal buka monitoring permohonan token\n" + \
                "Error message : "+str(e)
            print(message)
            return "no", message

    def get_history_montok(self, tipe_pencarian: str = "0", id_pencarian: str = "0"):
        try:
            # klik dropdown kategori search
            btnKategori = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/form/table/tbody/tr[3]/td/fieldset/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/img"))
            )
            btnKategori.click()
            print("Berhasil klik")
            time.sleep(1)
            # get semua child element dulu
            parentCategories = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "x-combo-list-item"))
            )
            print("Panjang Array : "+str(len(parentCategories)))
            print(str(len(parentCategories)))
            kategori = "PER IDPEL"
            if (tipe_pencarian == "0"):
                kategori = "PER IDPEL"
            else:
                kategori = "PER NOMOR METER"
            for items in parentCategories:
                if (items.text == kategori):
                    items.click()
                    break
            print("Berhasil klik pilihan dropdown")
            tfIdpel = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/form/table/tbody/tr[3]/td/fieldset/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input"))
            )
            tfIdpel.send_keys(id_pencarian)
            print("Entry Idpel berhasil")
            btnFilter = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/form/table/tbody/tr[4]/td/div/div/div[2]/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]"))
            )
            # Klik search idpel
            btnFilter.click()
            print("Berhasil klik Filter")
            # Get semua kct nya
            try:
                kctrows = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "x-grid3-row"))
                )
                print("panjang rows : "+str(len(kctrows)))
                if (len(kctrows) > 0):
                    time.sleep(1)
                    message = "berhasil get monitoring permohonan token"
                    # Coba get nilai kolomnya
                    for i in range(len(kctrows)):
                        print("\nKCT ke - "+str(i+1))
                        try:
                            cell_nomor_agenda = WebDriverWait(self.driver, 2).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/form/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(i+1)+"]/table/tbody/tr/td[1]/div")))
                            )
                            cell_tgl_transaksi = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/form/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(i+1)+"]/table/tbody/tr/td[9]/div")))
                            )
                            cell_jenis_transaksi = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/form/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(i+1)+"]/table/tbody/tr/td[10]/div")))
                            )
                            cell_status_agenda = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/form/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(i+1)+"]/table/tbody/tr/td[14]/div")))
                            )
                            cell_petugas = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/form/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(i+1)+"]/table/tbody/tr/td[25]/div")))
                            )
                            cell_unit = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, ("/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/form/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div["+str(i+1)+"]/table/tbody/tr/td[28]/div")))
                            )
                            # tanggal jatuh tempo
                            print("Nomor Agenda : " +
                                  cell_nomor_agenda.text + " Tgl Transaksi : "+cell_tgl_transaksi.text)
                            message = message+"No Agenda : "+cell_nomor_agenda.text + \
                                " Tgl Transaksi : "+cell_tgl_transaksi.text+" Jenis Transaksi : " + \
                                cell_jenis_transaksi.text+" Status Agenda : : "+cell_status_agenda.text + \
                                " Petugas : "+cell_petugas.text+" Kd Unit : "+cell_unit.text+"\n"
                        except Exception:
                            pass
                    return "yes", message
                else:
                    message = "Jumlah permohonan token = 0"
                    return "yes", message
            except Exception as e:
                message = "gagal get monitoring permohonan token\nError Message : " + \
                    str(e)
                print(message)
                return "no", message
        except Exception as e:
            message = "gagal get kategori permohonan token\nError Message : " + \
                str(e)
            print(message)
            return "no", message

    def buka_web_tagsus(self, kode_unit_user:str, tahun_bulan:str):
        print(kode_unit_user)
        print(tahun_bulan)
        try:
            link = "https://ap2t.pln.co.id/BillingTerpusatAP2TNew1-dr/ReportServlet?jenislaporan=getlaporantsgab&report=report/NONREK/rpt_ts_daftar_realisasi_pendapatan_penetapan_ts.xls&unitup=SEMUA&unitap="+\
                    str(kode_unit_user)+\
                        "&unitupi=32&jenislap=DAFTAR%20REALISASI%20PENDAPATAN%20PENETAPAN%20TAGIHAN%20SUSULAN%20(TUNAI%20DAN%20ANGSURAN)&thbl="+\
                            str(tahun_bulan)
            print("Membuka halaman AP2T")
            driver = self.driver
            # Maximize page
            driver.maximize_window()
            driver.get(link) #ganti nanti link ini
            time.sleep(5)
            message = "Tagsus Berhasil di Download"
            print(message)
            return "yes", message
        except Exception as e:
            message = "Gagal Donwload Laporan TS\nMessage Error : \n"+str(e)
            print(message)
            print("Error message : ", e)
            time.sleep(3)
            return "no", message
        
    def buka_monitoring_ts(self,link_spreadsheet,sheet_name):
        print("Membuka spreadsheet monitoring TS")
        try:
            driver = self.driver
            # Maximize page
            driver.maximize_window()
            driver.get(link_spreadsheet) #ganti nanti link ini
            time.sleep(3)
            #coba klik REPORT HARIAN
            try:
                print("Mencoba buka TAB REPORT HARIAN")
                #klik tab
                tab_report_harian = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[4]/div/div[4]/table/tbody/tr[2]/td[3]/div/div[3]/div/div[3]"))
                )
                tab_report_harian.click()
                time.sleep(5) #bisa di ganti sesuai kebutuhan
                message = "Berhasil buka tab REPORT HARIAN"
                return "yes",message
            except Exception as e:
                message = "Gagal buka Tab REPORT HARIAN\nMessage Error : \n"+str(e)
                print(message)
                return "no",message
        except Exception as e:
            message = "Gagal buka Spreadsheet\nMessage Error : \n"+str(e)
            print(message)
            return "no",message
        message = "Berhasil buka spreadsheet"
        print(message)
        return "yes",message

class ACMT:
    def __init__(self, filepatchromedriver, download_dir, user_options, url_acmt):
        pm = Parameter()
        self.filepathchromedriver = filepatchromedriver
        self.download_dir = download_dir
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(user_options)
        chrome_options.add_argument(pm.ignore_ssl_errors)
        chrome_options.add_argument(pm.ignore_certificate_errors)
        self.url_acmt = url_acmt
        self.driver = webdriver.Chrome(self.filepathchromedriver)
        self.tipe = "ACMT"

    def open_acmt(self):
        print("Membuka halaman "+self.tipe)
        driver = self.driver
        # Maximize page
        driver.maximize_window()
        # go to ap2t url
        try:
            driver.get(self.url_acmt)
            time.sleep(2)
            message = self.tipe + " Berhasil di buka"
            print(message)
            return "yes", message
        except Exception as e:
            message = "Gagal membuka "+self.tipe+"\nError message : " + str(e)
            print(message)
            return "no", message

    def login_acmt(self, username_acmt: str, password_acmt: str):
        self.driver.maximize_window()
        try:
            username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div/div[1]/div[1]/div/input"))
            )
            username.send_keys(username_acmt)  # sisa ganti jadi variabel
            password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[1]/div/input"))
            )
            password.send_keys(password_acmt)  # sisa ganti jadi variabel
            btnlogin = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button"))
            )
            btnlogin.click()
            time.sleep(3)
            # cobba identifikasi tombol logout
            try:
                log_out = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button"))
                )
                message = "Berhasil login "+self.tipe
                print(message)
                return "yes", message
            except Exception as e:
                message = "Gagal login "+self.tipe+"\nMessage Error : "+str(e)
                print(message)
                return "no", message
        except Exception as e:
            message = "Gagal login ACMT\nMessage Error : "+str(e)
            print(message)
            return "no", message

    def buka_informasi_pelanggan(self, infopelanggan: str):
        try:
            opsi_info_pelanggan = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/div/table/tbody/tr/td/div/table/tbody/tr/td/div[7]/div[1]/span[2]"))
            )
            # Definisi objek Action Chain for double click
            # double click info
            action = ActionChains(self.driver)
            action.double_click(opsi_info_pelanggan).perform()
            time.sleep(1)
            try:
                informasi_list = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/div/table/tbody/tr/td/div/table/tbody/tr/td/div[7]/div[2]/div[1]/div/span[2]"))
                )
                informasi_list.click()
                time.sleep(1)
                # Ekstract data
                tvIdpel = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[1]/div[1]/div/input"))
                )
                tvIdpel.send_keys(infopelanggan)
                tvIdpel.send_keys(Keys.RETURN)
                time.sleep(1)
                namaacmt = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[2]/div[1]/div/input"))
                )
                alamatacmt = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[3]/div[1]/div/textarea"))
                )
                unitacmt = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[4]/div[1]/div/input"))
                )
                tarifacmt = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[5]/div[1]/div/input"))
                )
                dayaacmt = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[6]/div[1]/div/input"))
                )
                nomormeteracmt = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[7]/div[1]/div/input"))
                )
                kddkacmt = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[8]/div[1]/div/input"))
                )
                garduacmt = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/form/fieldset[1]/div/div[9]/div[1]/div/input"))
                )
                nama = "Nama : "+namaacmt.get_attribute("value")+"\n"
                alamat = "Alamat : "+alamatacmt.get_attribute("value")+"\n"
                unit = "Kode Unit : "+unitacmt.get_attribute("value")+"\n"
                tarif = "Tarif : "+tarifacmt.get_attribute("value")+"\n"
                daya = "Daya : "+dayaacmt.get_attribute("value")+"\n"
                nomormeter = "Nomor Meter ACMT : " + \
                    nomormeteracmt.get_attribute("value")+"\n"
                kddk = "Kode Kedudukan : "+kddkacmt.get_attribute("value")+"\n"
                gardu = "Kode Gardu : "+garduacmt.get_attribute("value")
                # Merge info
                informasi = nama+alamat+unit+tarif+daya+nomormeter+kddk+gardu
                message = "Berhasil buka Informasi pelanggan"
                return "yes", informasi, message
            except Exception as e:
                message = "Gagal cari informasi pelanggan\nMessage Error : " + \
                    str(e)
                informasi = "null"
                return "no", informasi, message
        except Exception as e:
            message = "Gagal buka informasi pelanggan\nMessage Error : "+str(e)
            informasi = "null"
            return "no", informasi, message


# Create class for scraping


class Amicon(webdriver.Chrome):
    url = "https://amicon.pln.co.id/#/dashboard_technical"

    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

        base_dir = os.path.join(os.getcwd(), 'data')
        self.download_dir = os.path.join(base_dir, 'source')

        options = webdriver.ChromeOptions()

        # Setting cache di komputer server
        user_options = pm.user_browser_cache

        options.add_argument(user_options)
        options.add_argument('--disable-gpu')
        options.add_argument("enable-automation")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        # Passing SSL Security
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")

        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        super(Amicon, self).__init__(
            # executable_path=os.path.join(self._driver_path, 'chromedriver.exe'),
            options=options)

        # memberikan waktu menunggu halaman terload
        self.implicitly_wait(10)

    def first_page(self):
        self.get(self.url)
        self.maximize_window()

    def login(self):
        time.sleep(5)
        user_elm = self.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Username"]')
        user_elm.send_keys(self._username)

        pwd_elm = self.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Password"]')
        pwd_elm.send_keys(self._password)
        time.sleep(2)
        self.save_captcha(filename='captcha.png')
        captcha = self.read_captcha('captcha.png')
        time.sleep(2)

        # captcha input
        captcha_inp = self.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Enter Code"]')
        captcha_inp.send_keys(captcha)

        login_btn = self.find_element(
            By.CSS_SELECTOR, 'button[class="btn login_btn"]')
        login_btn.click()

    def cek_login(self):
        # cek apakah amicon sudah dalam posisi terlogin atau belum
        time.sleep(5)
        try:
            btn_search = WebDriverWait(self, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/app-dashboard/div/main/div/app-monitoring/div/div[1]/div/div/dx-form/div/div/div/div/div/div[2]/div/div/div/dxi-item/dx-button")))
            message = "Sudah login"
            return "yes", message
        except Exception as e:
            message = "Tidak login"
            print(message, "\nMessage Error :", str(e))
            return "no", message

    def refresh_captcha(self):
        time.sleep(1)
        refresh = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[title="Refresh Code"]')))
        # driver.find_element(By.CSS_SELECTOR, 'button[title="Refresh Code"]')
        refresh.click()
        time.sleep(3)

    def save_captcha(self, filename):
        # canvas = driver.find_element(By.ID, 'myCanvas')
        canvas = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located(
                (By.ID, 'myCanvas')
            )
        )
        # get the canvas as a PNG base64 string
        canvas_base64 = self.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);", canvas)

        # decode
        canvas_png = base64.b64decode(canvas_base64)

        # save to a file
        with open(filename, 'wb') as f:
            f.write(canvas_png)

    @ staticmethod
    def read_captcha(filename):
        reader = easyocr.Reader(gpu=True,
                                lang_list=['en', 'id'])  # this needs to run only once to load the model into memory
        result = reader.readtext(filename)
        return result[0][1]

    def click_monitoring(self):
        self.find_element(
            By.XPATH, '/html/body/app-dashboard/div/div/nav/ul/li[7]').click()
        time.sleep(1)

    def click_load_profile(self):
        self.find_element(
            By.CSS_SELECTOR, 'a[href="#/monitoring/loadprofile"]').click()
        time.sleep(1)

    def click_search(self):
        time.sleep(3)
        # click search
        try:
            btn_search = WebDriverWait(self, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/app-dashboard/div/main/div/app-monitoringloadprofile/div[2]/div[2]/div/div[2]/div[1]/dx-form/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/dxi-item/dx-button")))
            # btn_search.click()
            self.execute_script("arguments[0].click();", btn_search)
        except Exception as e:
            print("Gagal klik search\nMessage Error : ", str(e))
        # self.find_element(
        #     By.CSS_SELECTOR, 'dx-button[aria-label="Search"]').click()
        # print()
        time.sleep(1)

    def pilih_gardu(self, id_gardu):
        time.sleep(3)
        # click filter
        input_idp = self.find_element(By.XPATH,
                                      '//*[@id="gridContainer"]/div/div[5]/div[2]/table/tbody/tr[2]/td[5]/div/div[2]/div/div/input')
        input_idp.click()

        # masukan id gardu
        input_idp.send_keys(id_gardu)
        # click details
        self.find_element(By.CSS_SELECTOR, f'i[id="btn{id_gardu}"]').click()
        time.sleep(0.5)
        self.find_element(By.XPATH, '//span[text()="Detail"]').click()
        time.sleep(2)

    def pilih_tanggal(self):
        # isi tanggal
        hari_ini = datetime.datetime.now().strftime('%d/%m/%Y')
        # 10 hari yang lalu
        hari_awal = (datetime.datetime.now() -
                     datetime.timedelta(days=10)).strftime('%d/%m/%Y')
        tgl_awal = self.find_element(By.CSS_SELECTOR, '[id$=startDate]')
        tgl_awal.clear()
        tgl_awal.send_keys(hari_awal)
        ActionChains(self).send_keys(Keys.ENTER).perform()

        tgl_akhir = self.find_element(By.CSS_SELECTOR, '[id$=endDate]')
        tgl_akhir.clear()
        tgl_akhir.send_keys(hari_ini)
        ActionChains(self).send_keys(Keys.ENTER).perform()

        # click search
        self.find_element(By.CSS_SELECTOR, 'dx-button[icon="search"]').click()
        time.sleep(3)

    def export_to_excel(self):
        # sebelum di download hapus dulu file yang ada di foldernya
        print("Mencari load profile detail .xlsx")
        try:
            os.remove(os.path.join(self.download_dir,
                      'Load Profile Detail.xlsx'))
            print("Berhasil menghapus load profile detail.xlsx")
        except FileNotFoundError:
            pass

        try:
            btn_export = WebDriverWait(self, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/app-dashboard/div/main/div/app-monitoringloadprofile/div[2]/div[2]/div/div[2]/app-detailloadprofile/div/div[3]/div/dx-data-grid/div/div[4]/div/div/div[3]/div[1]/div/div")))
            self.execute_script("arguments[0].click();", btn_export)
            # btn_export.click()
            # click export to excel
            # self.find_element(
            #     By.CSS_SELECTOR, 'div[title="Export all data"]').click()
        except Exception as e:
            print("Gagal klik export to excel\nError Message : ", str(e))

        # open_excel = self.find_element(By.XPATH, '//*[@id="btnOpen"]')
        # open_excel.click()

        # chek file
        while not os.path.exists(os.path.join(self.download_dir, 'Load Profile Detail.xlsx')):
            time.sleep(2)
            # print('download selesai')
        time.sleep(1)

    def download_data(self, daftar_gd: list):
        self.first_page()
        status, message = self.cek_login()
        print(message)
        if (status != "yes"):
            self.login()
        self.click_monitoring()
        self.click_load_profile()
        berhasil = []
        gagal = []
        # self.implicitly_wait(15)
        for gd in daftar_gd:
            try:
                time.sleep(1)
                self.click_search()
                self.pilih_gardu(gd)
                self.pilih_tanggal()
                # scroll ke bawah
                # pyautogui.press("down", presses=10)
                self.export_to_excel()
                post_data(gd)
                print(f'{gd}: berhasil di update')
                berhasil.append(gd)
                self.refresh()
            except:
                self.refresh()
                print(f'{gd}: Gagal')
                gagal.append(gd)
            # time.sleep(1)
        print('Selesai mengupdate data')
        self.quit()
        return {'berhasil': berhasil, 'gagal': gagal}

class Helper:
    def delete_file(folder_path,filename_and_name_extension):
        file_path = os.path.join(folder_path, filename_and_name_extension)
        message = ""
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            message = f"The file '{filename_and_name_extension}' Berhasil di hapus."
            print(message)
            return "yes", message
        else:
            message = f"The file '{filename_and_name_extension}' File tidak ditemukan."
            print(message)
            return "no",message
        
    
#Helper.delete_file(r'data\downloads','ReportServlet.xls')