from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

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
        time.sleep(2)

    def search_contact(self,contact_name:str):
        try:
            #Klik serch contact
            searched_contact = WebDriverWait(driver=self.driver, timeout=2).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]/p"))
            )
            searched_contact.click()
            time.sleep(1)
            #Masukkan nama yang di cari
            searched_contact.send_keys(contact_name)
            print("berhasil ketik nama")
            time.sleep(1)
            #Klik contact yang dicari
            searched_contact = WebDriverWait(driver=self.driver, timeout=2).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div[3]/div[1]/div/div/div[1]/div/div"))
            )
            searched_contact.click()
            message  = "Berhasil menemukan contact"
            print(message)
            return "yes",message
        except Exception as e:
            message = "Gagal Search contact\nMessage Error : \n"+str(e)
            return "no",message
    def send_wa_messages(self,messages : str):
        try:
            #Klik messge box chat
            sendMessage = WebDriverWait(driver=self.driver, timeout=2).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p"))
            )
            sendMessage.click()
            #Masukkan chat
            sendMessage.send_keys(messages)
            time.sleep(1)
            #Klik tombol kirim chat
            sendMessage = WebDriverWait(driver=self.driver, timeout=2).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"))
            )
            sendMessage.click()
            message = "Berhasil mengirim chat"
            print(message)
            return "yes",message
        except Exception as e:
            message = "Gagal mengirim chat\nMessage error : \n"+str(e)
            print(message)
            return "no",message
        