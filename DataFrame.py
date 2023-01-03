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
