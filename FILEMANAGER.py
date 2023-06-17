
class filemanager():
    def take_screenshoot(direktori: str, file_name: str, driver):
        print("Memulai screenshoot")
        driver.save_screensoot(direktori+"\\fotoct.png")

    def send_photos(self, url_file_path):
        files = {"photo": open(url_file_path, "rb")}
        return files
