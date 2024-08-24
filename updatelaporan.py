import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parameter import Parameter
from FILEMANAGER import filemanager
pm = Parameter()

def run_spreadsheet_task():
    user_data = "user-data-dir=C:\\Users\\Core i7\\AppData\\Local\\Google\\Chrome\\User Data"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
    })

    options.add_argument(user_data)

  

    # URL Spreadsheet Google Anda
    SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1YLahMzMHne2g_dB7t_Vc5jMY1Zn7ZBoEUfdDWKzl-iw/edit?gid=1666680073#gid=1666680073"

    # Inisialisasi WebDriver dengan opsi
    service = Service(executable_path=pm.filepathchromedriver)
    #Setting parameter service untuk versi yang baru
    driver = webdriver.Chrome(
        service=service, options=options)

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
        sub_menu_mt_image = "data\\btn_wa\\macros1.png"  # Ganti dengan path ke file gambar screenshot Anda
        sub_menu_mt_location = pyautogui.locateCenterOnScreen(image=sub_menu_mt_image,confidence=0.7)
        
        if sub_menu_mt_location:
            pyautogui.click(sub_menu_mt_location)
        else:
            print("Gambar sub-menu 'macros1' tidak ditemukan di layar.")

        # Tunggu beberapa detik agar sub-sub-menu muncul
        time.sleep(2)

        # Menggunakan pyautogui untuk klik sub-sub-menu yang memiliki aria-activedescendant="f1bjz5:1yz" atau aria-own="f1bjz5:1yz"
        sub_sub_menu_image = "data\\btn_wa\\fungsiscrap.png"  # Ganti dengan path ke file gambar screenshot Anda
        sub_sub_menu_location = pyautogui.locateCenterOnScreen(image=sub_sub_menu_image,confidence=0.7)

        #Take Screenshoot
        driver.save_screenshot(pm.filepathct+"update_uid.png")
        time.sleep(5)
        
        if sub_sub_menu_location:
            pyautogui.click(sub_sub_menu_location)
        else:
            print("Gambar sub-sub-menu 'fungsi' tidak ditemukan di layar.")
        #Tutup driver
        driver.quit()
        return True

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        #Tutup driver
        driver.quit()
        return False

    

def open_dashboard_uid():
    user_data = "user-data-dir=C:\\Users\\Core i7\\AppData\\Local\\Google\\Chrome\\User Data"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
    })

    options.add_argument(user_data)

    # URL Spreadsheet Google Anda
    SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1YLahMzMHne2g_dB7t_Vc5jMY1Zn7ZBoEUfdDWKzl-iw/edit?gid=519149646#gid=519149646"
    # Inisialisasi WebDriver dengan opsi
    service = Service(executable_path=pm.filepathchromedriver)
    #Setting parameter service untuk versi yang baru
    driver = webdriver.Chrome(
        service=service, options=options)

    try:
        # Buka URL Spreadsheet Google
        driver.get(SPREADSHEET_URL)

        # Tunggu halaman sepenuhnya dimuat
        driver.implicitly_wait(5)  # Tunggu hingga 60 detik untuk elemen dimuat
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
