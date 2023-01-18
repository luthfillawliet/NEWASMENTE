import pandas as pd
from parameter import Parameter

pm = Parameter()


class dataframe():

    def get_userlink_bykodeunit(self, kdunit: str, jenis_user: str, part_link_awal: str, part_link_akhir: str):
        try:
            df = pd.read_excel(pm.filepathlistuser)
            print(df)
            # get nip uSER
            list_username = df[df["KODE_UNIT"] == int(kdunit)]
            username = list_username[list_username["Jabatan"]
                                     == jenis_user]["NIP"]
            password = list_username[list_username["Jabatan"]
                                     == jenis_user]["Password_AP2T"]
            link = part_link_awal + \
                username.item()+part_link_akhir
            # print("Username : ", username, "\nPassword : ", pasword)
            print(link)
            print("Length user : ", len(username.item()),
                  "\nLength password : ", len(password.item()), "(", password.item(), ")")
            message = "Berhasil get link dan username - password"
            return link, username.item(), password.item()
        except Exception as e:
            message = "Gagal ambil username, password dan get link, periksa File Excel dan kode unit\Message Error : " + e
            print(message)
            return link, "null", "0"

    def get_authenticated_user(self, filepathlistuser: str):
        try:
            # coba get list user dari database
            df = pd.read_excel(io=filepathlistuser,
                               sheet_name=pm.sheetname_listuserid)
            print(df)
            list_id = df["chat_id"].values.tolist()
            message = "Berhasil get list authenticated user"
            print(message)
            return "yes", list_id, message
        except Exception as e:
            list_id = []
            message = "Lst id gagal di ambil\nMessage Error : "+str(e)
            print(message)
            return "no", list_id, message

    def get_kode_unit_user(self, chat_id: int):
        try:
            df = pd.read_excel(io=pm.filepathlistuser,
                               sheet_name=pm.sheetname_listuserid)
            selected_row = df[df["chat_id"] == chat_id]
            print(selected_row)
            print("kode unit selected : ", selected_row["kode_unit"].item())
            message = "Berhasil get kode unit chat id"
            print(message)
            return "yes", selected_row["kode_unit"].item(), message
        except Exception as e:
            message = "Gagal mengambil kode unit user\nMessage Error : "+str(e)
            return "no", "null", message

    def get_user_acmt(self):
        try:
            df = pd.read_excel(io=pm.filepathlistuser, sheet_name="Sheet1")
            selected_row = df[df["Akun"] == "ACMT"]
            username = selected_row["NIP"].item()
            password = selected_row["Password_AP2T"].item()
            print("Username : ", username, "Password : ", password)
            return "yes", username, password
        except Exception as e:
            message = "Gagal read list user acmt\nMessage Error : "+str(e)
            print(message)
            return "no", "null", "null"

    def get_jumlah_klik_resetimei(self, kodeunit_cari: str):
        df = pd.read_excel(io=pm.filepathlistuser, sheet_name="listulp")
        rows_klik = df[df["kode_unit"] == kodeunit_cari]
        jumlah_perulangan = rows_klik["no"].item()
        print("jumlah klik : ", jumlah_perulangan)
        print(type(jumlah_perulangan))
        return int(jumlah_perulangan)
