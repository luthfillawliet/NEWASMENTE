import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_spreadsheet_task():
    user_data = "user-data-dir=C:\\Users\\Core i7\\AppData\\Local\\Google\\Chrome\\User Data"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
    })

    options.add_argument(user_data)
    options.add_argument("--profile-directory=Profile 1")
  

    # URL Spreadsheet Google Anda
    SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1UtX6vH7hhiyC2tZ9fBtGPQ_GSrzQeEv-c97OjWnqW2c/edit?usp=sharing"

    # Inisialisasi WebDriver dengan opsi
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Buka URL Spreadsheet Google
        driver.get(SPREADSHEET_URL)

        # Tunggu halaman sepenuhnya dimuat
        driver.implicitly_wait(60)  # Tunggu hingga 60 detik untuk elemen dimuat

        # Temukan dan klik menu "Extensions"
        extensions_menu = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "docs-extensions-menu"))
        )

        # Pastikan elemen berada di viewport sebelum mengklik
        driver.execute_script("arguments[0].scrollIntoView();", extensions_menu)
        extensions_menu.click()

        # Tunggu beberapa detik agar dropdown muncul
        time.sleep(2)

        # Menggunakan pyautogui untuk klik sub-menu yang memiliki aria-activedescendant=":mt"
        sub_menu_mt_image = "macros1.png"  # Ganti dengan path ke file gambar screenshot Anda
        sub_menu_mt_location = pyautogui.locateCenterOnScreen(sub_menu_mt_image)
        
        if sub_menu_mt_location:
            pyautogui.click(sub_menu_mt_location)
        else:
            print("Gambar sub-menu 'macros1' tidak ditemukan di layar.")

        # Tunggu beberapa detik agar sub-sub-menu muncul
        time.sleep(2)

        # Menggunakan pyautogui untuk klik sub-sub-menu yang memiliki aria-activedescendant="f1bjz5:1yz" atau aria-own="f1bjz5:1yz"
        sub_sub_menu_image = "fungsiscrap.png"  # Ganti dengan path ke file gambar screenshot Anda
        sub_sub_menu_location = pyautogui.locateCenterOnScreen(sub_sub_menu_image)
        
        if sub_sub_menu_location:
            pyautogui.click(sub_sub_menu_location)
        else:
            print("Gambar sub-sub-menu 'fungsi' tidak ditemukan di layar.")

        # Tambahkan tindakan lain jika diperlukan

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    # Menjaga browser tetap terbuka dengan input user
    print("Browser akan tetap terbuka. Tekan Enter untuk menutup.")
    input("Tekan Enter untuk keluar dan menutup browser...")
    driver.quit()