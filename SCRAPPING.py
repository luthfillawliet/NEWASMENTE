import os
import stat
import win32api
import win32con
import time
import pyautogui
import pandas as pd
import pyperclip
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Tentukan lokasi folder unduhan
download_dir = r"data\downloads\EIS"

# Tentukan lokasi file gambar 'keep_button_image.png' dan 'keep_anyway_image.png'
keep_button_image_path = r"D:\learn-selenium\download.png"
keep_anyway_image_path = r"D:\learn-selenium\keep.png"

# Inisialisasi ChromeOptions
user_data = "user-data-dir=C:\\Users\\lenovo\\AppData\\Local\\Google\\Chrome\\User Data"
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,
    "profile.default_content_setting_values.automatic_downloads": 1
})

options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-web-security")
options.add_argument(user_data)
options.add_argument("--profile-directory=Profile 12")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

# Fungsi untuk menghapus file jika ada
def delete_existing_file(file_path):
    if os.path.exists(file_path):
        try:
            os.chmod(file_path, stat.S_IWRITE)
            win32api.SetFileAttributes(file_path, win32con.FILE_ATTRIBUTE_NORMAL)
            os.remove(file_path)
            print(f"Deleted existing file: {file_path}")
        except Exception as e:
            print(f"An error occurred while deleting file: {e}")

try:
    delete_existing_file(os.path.join(download_dir, "GV.xls"))

    driver.get('http://eis.ap2t.pln.co.id/eis/login.aspx')
    driver.maximize_window()

    try:
        user_id_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'txtUserid'))
        )
        password_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'TxtPWDx'))
        )
    except TimeoutException:
        print("Timed out waiting for user ID and password fields to load")
        driver.quit()
        exit()

    user_id_box.clear()
    password_box.clear()
    user_id_box.send_keys('94171287ZY')
    password_box.send_keys('Panjang@1025')
    login_button = driver.find_element(By.ID, 'ext-gen24')
    login_button.click()

    layanan_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ext-gen28')))
    layanan_button.click()

    detil_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ext-gen165')))
    detil_button.click()

    time.sleep(30)

    iframe = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'mondetil_IFrame')))
    driver.switch_to.frame(iframe)
    print("Switched to iframe successfully")

    div_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="ext-gen49" and .//input[@id="cboJenis_Value" and @value="SEMUA"]]'))
    )

    if div_element.is_displayed() and div_element.is_enabled():
        div_element.click()
        print("Clicked to open dropdown PS/PD/PB")

        pd_options = driver.find_elements(By.XPATH, '//div[contains(@class, "x-combo-list-item")]')
        for option in pd_options:
            print(option.text)
            if option.text.strip() == 'PD':
                option.click()
                print("Clicked on PD option")
                break

        loadData_button = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.ID, 'ext-gen62')))
        loadData_button.click()
        print("Clicked Load Data button")

        loadExcel_button = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.ID, 'ext-gen107')))
        loadExcel_button.click()
        print("Clicked Excel button")

        time.sleep(50)

        try:
            keep_button_location = pyautogui.locateCenterOnScreen(keep_button_image_path, confidence=0.9)
            if keep_button_location:
                pyautogui.click(keep_button_location)
                print("Clicked on button using download.png")

                time.sleep(70)
                keep_anyway_location = pyautogui.locateCenterOnScreen(keep_anyway_image_path, confidence=0.9)
                if keep_anyway_location:
                    pyautogui.click(keep_anyway_location)
                    print("Clicked on button using keep.png")
                else:
                    print("Not found using keep.png")
            else:
                print("Not found using download.png")
        except Exception as e:
            print(f"An error occurred while trying to click the Keep button: {e}")
        time.sleep(90)

        # Langsung ke proses membuka file Excel dan menyalin isinya ke clipboard
        excel_file_path = os.path.join(download_dir, "GV.xls")
        subprocess.Popen(['start', 'excel', excel_file_path], shell=True)
        time.sleep(50)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(90)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(90)
        copied_data = pyperclip.paste()
        if copied_data:
            print("Data copied to clipboard successfully.")
        else:
            print("Clipboard is empty.")
            exit()

        # Buka spreadsheet dan tempel data
        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1OSXWgWS7_RD9Tb9VKYtDV_LmD1Z9KGVu0mdlSl6DhyQ/edit?gid=1554913411#gid=1554913411'
        driver.get(spreadsheet_url)
        driver.maximize_window()
        time.sleep(60)

        # Pilih sel A1 di Google Sheets
        try:
            sheet = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.docs-sheet-active-tab'))
            )

            # Klik sel A1
            sheet.click()

            # Tunggu sebentar
            time.sleep(60)

            # Gunakan pyautogui untuk menempel data ke Google Sheets
            pyautogui.hotkey('ctrl', 'v')

            # Tunggu beberapa detik untuk memastikan data tertempel
            time.sleep(90)

            # Tambahan pengecekan apakah data tertempel dengan benar
            cells = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.waffle-cell'))
            )
            if cells:
                print("Data pasted to Google Sheets successfully.")
            else:
                print("Data paste failed. No data found in Google Sheets.")

        except Exception as e:
            print(f"An error occurred while pasting data: {e}")
    else:
        print("Div element is not visible or enabled.")
    
except TimeoutException as e:
    print(f"TimeoutException: {e}")
except NoSuchElementException as e:
    print(f"NoSuchElementException: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.switch_to.default_content()
    #driver.quit()
