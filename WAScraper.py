from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pyautogui
import pyperclip
from DataFrame import dataframe

class WA:
    # Create class for scraping EIS
    def __init__(self, filepathchromedriver, download_dir, user_options,message :str, contact:str):
        self.filepatchromedriver = filepathchromedriver
        self.download_dir = download_dir
        self.user_options = user_options
        self.urlwa = "https://web.whatsapp.com/"
        # self.username_eis = username_eis
        # self.password_eis = password_eis
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--allow-running-insecure-content")
        # chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument(user_options)
        service = Service(executable_path=filepathchromedriver)
        #Setting parameter service untuk versi yang baru
        self.driver = webdriver.Chrome(
            service=service, options=chrome_options)
        
    def open_wa(self):
        driver = self.driver
        driver.get(self.urlwa)
        time.sleep(5)

    def search_contact(self,contact_name:str):
        try:
            #Klik serch contact
            cari_image_button = "C:\\Users\\CORE i7\\Documents\\GitHub\\NEWASMENTE\\data\\btn_wa\\Cari.png"
            cari_image_button = pyautogui.locateCenterOnScreen(cari_image_button, confidence=0.9)
            pyautogui.click(cari_image_button)
            time.sleep(3)
            #Masukkan nama yang di cari
            pyautogui.write(contact_name)
            print("berhasil ketik nama")
            time.sleep(3)
            contact_button_image_path = "data\\btn_wa\\"+contact_name+".png"
            try:
                contact_button_location = pyautogui.locateCenterOnScreen(contact_button_image_path, confidence=0.7)
                message  = "Berhasil menemukan contact"
                if contact_button_location:
                    pyautogui.click(contact_button_location)
                    print("Clicked on button using image")
            except:
                print("gagal klik foto")
            print(message)
            return "yes",message
        except Exception as e:
            message = "Gagal Search contact\nMessage Error : \n"+str(e)
            return "no",message
    def send_wa_messages(self,messages : str):
        try:
            #Klik messge box chat
            sendMessage = WebDriverWait(driver=self.driver, timeout=2).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]"))
            )
            sendMessage.click()
            #Masukkan chat
            sendMessage.send_keys(messages)
            time.sleep(1)
            #Klik tombol kirim chat
            sendMessage = WebDriverWait(driver=self.driver, timeout=2).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[2]/button"))
            )
            sendMessage.click()
            time.sleep(10)
            message = "Berhasil mengirim chat"
            print(message)
            return "yes",message
        except Exception as e:
            message = "Gagal mengirim chat\nMessage error : \n"+str(e) 
            print(message)
            return "no",message
        
    def image_wa_message(self,image_location_path:str,message : str):
        try:
            driver = self.driver
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf"][@data-tab="10"]'))
            )
            time.sleep(2)

            # Tekan tombol Enter untuk mengirim pesan
            message_box = driver.find_element(By.XPATH, '//div[@class="x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf"][@data-tab="10"]')

            #Klik logo attach
            x, y = pyautogui.locateCenterOnScreen("img/lampir.png", confidence= 0.9)
            pyautogui.moveTo(x, y, duration = 1)
            pyautogui.leftClick()
            time.sleep(2)

            #Klik tambah foto atau video
            x, y = pyautogui.locateCenterOnScreen("img/fto.png", confidence= 0.9)
            pyautogui.moveTo(x, y, duration = 2)
            pyautogui.leftClick()
            time.sleep(1)

            #Menyalin path lokasi gambar/image
            file_path = image_location_path # Ubah sesuai path yang diinginkan
            pyperclip.copy(file_path)
            pyautogui.sleep(2)
            pyautogui.hotkey("ctrl", "v")
            
            #Klik open foto utu
            pyautogui.sleep(1)
            x, y = pyautogui.locateCenterOnScreen("img/open.png", confidence= 0.9)
            pyautogui.moveTo(x, y, duration = 1)
            pyautogui.leftClick()
            pyautogui.sleep(1)
            
            #Klik logo kirim
            x, y = pyautogui.locateCenterOnScreen("img/send.png", confidence= 0.9)
            pyautogui.moveTo(x, y, duration = 1)
            pyautogui.leftClick()

            time.sleep(3)

            #Send Message
            pyautogui.write(message=message)
            time.sleep(3)
            #Klik logo kirim
            cari_image_send = "img/send.png"
            cari_image_send = pyautogui.locateCenterOnScreen(cari_image_send, confidence=0.9)

            print(f"Pesan berhasil dikirim")
            time.sleep(6) 
            
        except Exception as e:
            print(f"Gagal mengirim pesan")