import pandas as pd
from parameter import Parameter

pm = Parameter()


class dataframe():

    def get_userlink_bykodeunit(self, kdunit: str):
        df = pd.read_excel(pm.filepathlistuser)
        print(df)
        if (kdunit == "32111"):
            # print("Kode Unit terbaca : Panakkukang")
            # get nip uSER
            list_username = df[df["KODE_UNIT"] == int(kdunit)]
            username = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["NIP"]
            password = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["Password_AP2T"]
            link = pm.linkpengaduanct + \
                username.item()+pm.linkpengaduanct_2
            # print("Username : ", username, "\nPassword : ", pasword)
            print(link)
            print("Length user : ", len(username.item()),
                  "\nLength password : ", len(password.item()), "(", password.item(), ")")
            return link, username.item(), password.item()
        elif (kdunit == "32121"):
            print("Kode Unit terbaca : Mattoanging")
            list_username = df[df["KODE_UNIT"] == int(kdunit)]
            username = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["NIP"]
            password = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["Password_AP2T"]
            link = pm.linkpengaduanct + \
                username.item()+pm.linkpengaduanct_2
            # print("Username : ", username, "\nPassword : ", pasword)
            print(link)
            print("Length user : ", len(username.item()),
                  "\nLength password : ", len(password.item()), "(", password.item(), ")")
            return link, username.item(), password.item()
        elif (kdunit == "32131"):
            print("Kode Unit terbaca : Sungguminasa")
            # print("Kode Unit terbaca : Panakkukang")
            # get nip uSER
            list_username = df[df["KODE_UNIT"] == int(kdunit)]
            username = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["NIP"]
            password = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["Password_AP2T"]
            link = pm.linkpengaduanct + \
                username.item()+pm.linkpengaduanct_2
            # print("Username : ", username, "\nPassword : ", pasword)
            print(link)
            print("Length user : ", len(username.item()),
                  "\nLength password : ", len(password.item()), "(", password.item(), ")")
            return link, username.item(), password.item()
        elif (kdunit == "32141"):
            print("Kode Unit terbaca : Kalebajeng")
            # print("Kode Unit terbaca : Panakkukang")
            # get nip uSER
            list_username = df[df["KODE_UNIT"] == int(kdunit)]
            username = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["NIP"]
            password = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["Password_AP2T"]
            link = pm.linkpengaduanct + \
                username.item()+pm.linkpengaduanct_2
            # print("Username : ", username, "\nPassword : ", pasword)
            print(link)
            print("Length user : ", len(username.item()),
                  "\nLength password : ", len(password.item()), "(", password.item(), ")")
            return link, username.item(), password.item()
        elif (kdunit == "32151"):
            print("Kode Unit terbaca : Takalar")
            # print("Kode Unit terbaca : Panakkukang")
            # get nip uSER
            list_username = df[df["KODE_UNIT"] == int(kdunit)]
            username = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["NIP"]
            password = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["Password_AP2T"]
            link = pm.linkpengaduanct + \
                username.item()+pm.linkpengaduanct_2
            # print("Username : ", username, "\nPassword : ", pasword)
            print(link)
            print("Length user : ", len(username.item()),
                  "\nLength password : ", len(password.item()), "(", password.item(), ")")
            return link, username.item(), password.item()
        elif (kdunit == "32161"):
            print("Kode Unit terbaca : Malino")
            # print("Kode Unit terbaca : Panakkukang")
            # get nip uSER
            list_username = df[df["KODE_UNIT"] == int(kdunit)]
            username = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["NIP"]
            password = list_username[list_username["Jabatan"]
                                     == "TL TEKNIK"]["Password_AP2T"]
            link = pm.linkpengaduanct + \
                username.item()+pm.linkpengaduanct_2
            # print("Username : ", username, "\nPassword : ", pasword)
            print(link)
            print("Length user : ", len(username.item()),
                  "\nLength password : ", len(password.item()), "(", password.item(), ")")
            return link, username.item(), password.item()
