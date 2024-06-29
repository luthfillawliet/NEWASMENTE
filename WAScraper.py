from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        chrome_options.add_argument("--profile-directory=Profile 12")
        service = Service(executable_path=filepathchromedriver)
        #Setting parameter service untuk versi yang baru
        self.driver = webdriver.Chrome(
            service=service, options=chrome_options)
        
    def open_wa(self):
        driver = self.driver
        driver.get(self.urlwa)
        time.sleep(10)

    def choose_contact(self,contact_name:str):
        #/html/body/div[1]/div/div/div[2]/div[3]/div/div[3]/div[1]/div/div/div[12]/div/div/div/div[2]/div[1]/div[1]/div/span[1]