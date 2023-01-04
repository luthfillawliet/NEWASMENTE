import time
import os
import datetime

from parameter import Parameter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pywinauto.application import Application
from selenium.webdriver.support.ui import Select


class AP2T:
    def __init__(self, filepathchromedriver, filepathenkripsi, urlap2t, download_dir, filepathct, user_options):

        self.filepathchromedriver = filepathchromedriver
        self.filepathenkripsi = filepathenkripsi
        self.urlap2t = urlap2t
        self.download_dir = download_dir
        self.filepathct = filepathct
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

    def login_ap2t(self, username_ap2t, password_ap2t):
        print("uSERNAME : ", username_ap2t, "\PASSWORD : ", password_ap2t)
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
                message = "Gagal klk login"
                print(message)
                print("Error message : ", e)
                return "no", message
        except Exception as e:
            message = "Gagal login ap2t"
            print(message)
            print("Error Message : ", e)
            return "no", message

    def input_pengaduan_ct(self, id_pelanggan, petugas_dan_keterangan, link_pengaduan_ct):
        try:
            # Buka Tab baru
            self.driver.execute_script(
                "window.open('"+link_pengaduan_ct+"');")
            time.sleep(5)  # Bisa di ubah sesuai kebutuhan
            print("Berhasil buka tab permohonan pengaduan")
            try:
                # pindah tab ke tab pengaduan
                self.driver.switch_to.window(self.driver.window_handles[1])
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
                        (By.CLASS_NAME, "x-combo-list-inner"))
                )
                try:
                    # print(str(len(child_elements)))
                    print("Berhasil get child elements")
                    for items in parentCategories:
                        print(items.text)
                        if (items.text == "PERMINTAAN CLEAR TAMPER"):
                            # klik itemnya
                            items.click()
                            break
                    time.sleep(1)
                    # Input Petugas dan Keterangan
                    field_keterngan = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div/div/div/div[1]/div/div/div[2]/div/div/fieldset/div/div/div[4]/div[1]/textarea")
                        )
                    )
                    field_keterngan.send_keys(petugas_dan_keterangan)
                    time.sleep(1)
                    # pilih dropdown penyebab periksa
                    btnAlasan = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div/div/div/div[1]/div/div/div[2]/div/div/fieldset/div/div/div[9]/div[1]/div/img"))
                    )
                    btnAlasan.click()
                    time.sleep(3)
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
                        noAgenda = WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/form/div/div/div/div/div[1]/div/div/div[1]/div/div/fieldset/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input"))
                        )
                        nomoragenda = noAgenda.get_attribute("value")
                        # klik tombol success nya
                        btnSuccess = WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "/html/body/div[14]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button"))
                        )
                        btnSuccess.click()
                        print(nomoragenda)
                        time.sleep(1)
                        return ["yes", "Berhasil buat pengaduan", nomoragenda]
                    except:
                        message = "Gagal pilih dropdown penyebab"
                        print(message)
                        return ["no", message, 0]
                except:
                    message = "Gagal pilih menu pengaduan"
                    print(message)
                    return ["no", message, 0]
            except:
                message = "Gagal input pengaduan"
                print(message)
                return ["no", message, 0]
                # Buka Link Pengaduan Pelanggan CT
        except:
            message = "Gagal buka link pengaduan CT"
            print(message)
            return ["no", message, 0]

    def tindakan_pengaduan_ct(self, nomor_agenda, link_tindakan_pengaduan_ct):
        try:
            # Buka Tab baru
            self.driver.execute_script(
                "window.open('"+link_tindakan_pengaduan_ct+"');")
            time.sleep(5)  # Bisa di ubah sesuai kebutuhan
            try:
                # pindah tab ke tab pengaduan
                self.driver.switch_to.window(self.driver.window_handles[2])
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
                # save nomor agenda
                btnSaveT = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[2]/div/table/tbody/tr/td[1]/div/div/div/div/div[2]/div[1]/div/div/div/form/fieldset[3]/div/div[2]/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button"))
                )
                btnSaveT.click()
                time.sleep(1)
                message = "Berhasil menyimpan tindakan pengaduan"
                print(message)
                return ["yes", message, nomor_agenda]
            except:
                message = "Gagal entry tindakan pengaduan"
                print(message)
                return ["no", message, nomor_agenda]
        except:
            message = "Gagal Buka Halaman Tindakan pengaduan"
            print(message)
            return ["no", message, nomor_agenda]

    def aktivasi_ct(self, nomoragenda, link_aktivasi_meter):
        try:
            print("Memulai aktivasi token")
            self.driver.execute_script(
                "window.open('"+link_aktivasi_meter+"');")
            time.sleep(5)  # Bisa di ubah sesuai kebutuhan
            # pindah tab ke tab pengaduan
            self.driver.switch_to.window(self.driver.window_handles[3])
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
        except:
            message = "Gagal aktivasi token"
            print(message)
            return ["no", message, nomoragenda]

    def monitoring_token(self, tipe_pencarian, nomor_id, url_monitoring_token, url_cetak_token):
        # Buka link monitoring token

        # Tipe pencarian : 0, jika idpel, 1 jika nomor meter. dan 2 jika nomor agenda
        if (tipe_pencarian == 0):
            # Eksekusi pencarian berdasarkan Idpel
            print("Cari token berdasarkan Idpel")
            self.monitoring_cari_idpel(
                url_montok=url_monitoring_token, idpel=nomor_id)
            status, jumlahCT = self.get_jumlah_request(
                jenis_token="CLEAR TAMPER")
            nomoragenda = self.show_last_kct()
            if (nomoragenda != "0"):
                self.cetak_token(nomoragenda=nomoragenda,
                                 link_ct=url_cetak_token)
                return ["yes", "Cari token berdasarkan Idpel Berhasil"]
        elif (tipe_pencarian == 2):
            # Eksekusi pencarian berdasarkan Nomor Meter
            print("Cari token berdasarkan Nomor Meter")
        elif (tipe_pencarian == 3):
            # Eksekusi pencarian berdasarkan Nomor Agenda
            print("Cari token berdasarkan Nomor Agenda")
        else:
            # Kode dasar pencarian tidak dikenal
            print("Kode dasar pencarian tidak dikenal")

    def monitoring_cari_idpel(self, url_montok, idpel):
        try:
            # masukkan idpel
            self.driver.execute_script(
                "window.open('"+url_montok+"');")
            time.sleep(5)  # Bisa di ubah sesuai kebutuhan
            # pindah tab ke tab pengaduan
            # Ubah untuk testing dan run
            self.driver.switch_to.window(self.driver.window_handles[4])
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

    def take_screenshoot(self, direktori: str, file_name: str):
        print("Memulai screenshoot")
        time.sleep(3)
        # ganti jika tes dan running
        self.driver.switch_to.window(self.driver.window_handles[5])
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
                # Merge semua data
                dataPelanggan = id_pelanggan+nomor_meter + \
                    namapelanggan+tarif+daya+alamat+merk_meter+krn
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


class ACMT:
    def __init__(self, filepatchromedriver, download_dir, user_options, url_acmt):
        pm = Parameter()
        self.filepathchromedriver = filepatchromedriver
        self.download_dir = download_dir
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            user_options)
        chrome_options.add_argument(pm.ignore_ssl_errors)
        chrome_options.add_argument(pm.ignore_certificate_errors)
        self.url_acmt = url_acmt
        self.driver = webdriver.Chrome(self.filepathchromedriver)
        self.tipe = "ACMT"

    def open_acmt(self):
        print("Membuka halaman AP2T")
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

    def login_acmt(self, username: str, password: str):
        self.driver.maximize_window()
        try:
            username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div/div[1]/div[1]/div/input"))
            )
            username.send_keys("32131.vendor")  # sisa ganti jadi variabel
            password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[1]/div/input"))
            )
            password.send_keys("billmanbisa")  # sisa ganti jadi variabel
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
