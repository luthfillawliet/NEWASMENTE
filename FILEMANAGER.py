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
            return "yes",message
    def check_file(folder_path,filename_and_name_extension):
        file_path = os.path.join(folder_path, filename_and_name_extension)
        if os.path.exists(file_path):
            message = "File ditemukan"
            print(message)
            return True,message
        else:
            message = "File Tidak Ditemukan"
            print(message)
            return False, message
    @staticmethod
    def select_last_modified_files(path:str):
        # Path to the directory
        folder_path = path

        # Get a list of files in the directory with their modification time
        files = [(file, os.path.getmtime(os.path.join(folder_path, file))) for file in os.listdir(folder_path)]

        # Sort the files based on modification time (last modified will be at index 0)
        files.sort(key=lambda x: x[1], reverse=True)

        # Check if any files are present in the folder
        if files:
            most_recent_file = files[0][0]
            print(f"The most recently modified file is: {most_recent_file}")
            return "yes",most_recent_file
        else:
            print("No files found in the directory.")
            return "no",most_recent_file
    @staticmethod
    def rename_most_recent_file(path:str,most_recent_file:str,new_file_name_with_extension:str):
        try:
            # Rename the downloaded file
            downloaded_file_path = os.path.join(path, most_recent_file)
            new_file_path = os.path.join(path, new_file_name_with_extension)
            os.rename(downloaded_file_path, new_file_path)
            message = "Success Renaming Filename"
            print(message)
            return "yes",new_file_path,message
        except Exception as e:
            error_message = str(e)
            message = "Error modified filename\n Error Message : "+str(e)
            print(f"Error message : {error_message}")
            return "no","null",message
        
        
#pm = Parameter()
#filemanager.take_screenshoot_pixel(kiri_atas_layar_x=pm.kiri_atas_layar_x,kiri_atas_layar_y=pm.kiri_atas_layar_y,kanan_bawah_layar_x=pm.kanan_bawah_layar_x,kanan_bawah_layar_y=pm.kanan_bawah_layar_y)
path = "data//downloads"
[s,f] = filemanager.select_last_modified_files(path=path)
#[s,m] = filemanager.rename_most_recent_file(path=path,most_recent_file=f,new_file_name_with_extension="TUL 309 Lap 1.xls")