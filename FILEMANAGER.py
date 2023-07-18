import os
from PIL import ImageGrab
from parameter import Parameter
import time
class filemanager():
    def take_screenshoot(direktori: str, file_name: str, driver):
        print("Memulai screenshoot")
        driver.save_screensoot(direktori+"\\fotoct.png")
    
    def take_screenshoot_pixel(kiri_atas_layar_x : int,kiri_atas_layar_y : int,kanan_bawah_layar_x : int,kanan_bawah_layar_y : int):
        time.sleep(5)
        screenshot = ImageGrab.grab(bbox=(kiri_atas_layar_x, kiri_atas_layar_y, kanan_bawah_layar_x, kanan_bawah_layar_y))
        save_folder = "fotoct"
        # Create the folder if it doesn't exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        file_path = os.path.join(save_folder, "screenshot_ts.png")
        screenshot.save(file_path)
        #screenshot.show() # nda usah preview fotonya

    def send_photos(self, url_file_path):
        files = {"photo": open(url_file_path, "rb")}
        return files
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

#pm = Parameter()
#filemanager.take_screenshoot_pixel(kiri_atas_layar_x=pm.kiri_atas_layar_x,kiri_atas_layar_y=pm.kiri_atas_layar_y,kanan_bawah_layar_x=pm.kanan_bawah_layar_x,kanan_bawah_layar_y=pm.kanan_bawah_layar_y)