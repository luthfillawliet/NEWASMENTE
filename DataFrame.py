import pandas as pd
import openpyxl
import xlwt
from parameter import Parameter

pm = Parameter()


class dataframe():

    def baca_kct(self, filepath_kct_krn: str, id_pelanggan: int):
        try:
            df = pd.read_excel(filepath_kct_krn)
            # 321610005372
            idpel_search = int(id_pelanggan)
            indexfound = ""
            # get number of rows
            numrows = len(df.index)
            print(numrows)

            for i in range(numrows):
                data = df["IDPEL"][i]
                if (data == idpel_search):
                    indexfound = i
                    break
            kct1a = df["TOKEN_KCT1A"][indexfound]
            kct1b = df["TOKEN_KCT1B"][indexfound]
            kct2a = df["TOKEN_KCT2A"][indexfound]
            kct2b = df["TOKEN_KCT2B"][indexfound]
            petugasbaca = df["PETUGASBACA"][indexfound]
            tanggalbaca = df["TGLBACA"][indexfound]
            statusbaca = df["KETERANGAN_STATUS_BACA"][indexfound]
            message = "Status Baca Idpel "+str(idpel_search) + " : " + statusbaca + \
                "\n" + "Nama Petugas : " + \
                str(petugasbaca)+"\n" + "Tanggal baca : " + str(tanggalbaca) + \
                "\n" + "KCT 1A : " + str(kct1a) + "\n" + "KCT 1B : " + str(
                    kct1b)+"\n" + "KCT 2A : " + str(kct2a) + "\n" + "KCT 2B : " + str(kct2b)
            # message = "Status Baca : " + statusbaca + "\n" + "Nama Petugas : " + petugasbaca, "\n" + "Tanggal baca : " + str(tanggalbaca) + \
            #     "\n" + "KCT 1A : " + str(kct1a) + "\n" + "KCT 1B : " + str(kct1b) + \
            #     "\n" + "KCT 2A : " + str(kct2a) + "\n" + "KCT 2B : " + str(kct2b)
            print("idpelfound : ", indexfound)
            print(message)
            return "yes", message
        except Exception as e:
            message = "Gagal read file excel kct\nMessage Error : "+str(e)
            print(message)
            return "no", message

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

    def get_level_user_data(self, chat_id: int):
        try:
            df = pd.read_excel(io=pm.filepathlistuser,
                               sheet_name=pm.sheetname_listuserid)
            selected_row = df[df["chat_id"] == chat_id]
            print("Level user id ", chat_id, " : ",
                  selected_row["level"].item())
            message = "Berhasil get level user"
            return "yes", selected_row["level"].item(), message
        except Exception as e:
            message = "gagal get level user \nMessage Error : "+str(e)
            return "no", "null", message

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

    def get_last_row(self, filepathlistuser: str, sheetname: str):
        try:
            df = pd.read_excel(io=filepathlistuser,
                               sheet_name=sheetname)
            print("Baris akhir pada excel : ", str(len(df["no"])+1))
            nomor_rows = len(df["no"])+2
            message = "Berhasil get last row"
            print(message)
            return "yes", nomor_rows, message
        except Exception as e:
            message = "Gagal get last rows, harap periksa file sedang tidak digunakan" + \
                str(e)
            print(message)
            return "no", 0, message

    def write_data_userid(self, filepathlistuser: str, sheetname: str, row: int, chat_id: int = 0, kode_unit: int = 0, nama: str = "", nomor_telfon: str = "", level: str = "user"):
        # select the workbook
        try:
            workbook = openpyxl.load_workbook(filename=filepathlistuser)
            worksheet = workbook.get_sheet_by_name(sheetname)
            try:
                worksheet.cell(row=row, column=1).value = row-1
                worksheet.cell(row=row, column=2).value = chat_id
                worksheet.cell(row=row, column=3).value = kode_unit
                worksheet.cell(row=row, column=4).value = nama
                worksheet.cell(row=row, column=5).value = nomor_telfon
                worksheet.cell(row=row, column=6).value = level
                workbook.save(filepathlistuser)
                message = "Berhasil add user"
                print(message)
                return "yes", message
            except Exception as e:
                message = "Gagal add user\nMessage Error : "+str(e)
                print(message)
                return "no", message
        except Exception as e:
            message = "Gagal load excel\n"+str(e)
            print(message)
            return "no", message

    def log_data(self, chat_id: int, activity: str, time: str):
        pm = Parameter()
        try:
            status, last_row, message = self.get_last_row(
                filepathlistuser=pm.filepathlog, sheetname="log")
            if (status == "yes"):
                print("Last row : "+str(last_row))
                print(message)
                # Write number of rows
                workbook = openpyxl.load_workbook(filename=pm.filepathlog)
                worksheet = workbook.get_sheet_by_name("log")
                worksheet.cell(row=last_row, column=1).value = last_row-1
                worksheet.cell(row=last_row, column=2).value = chat_id
                worksheet.cell(row=last_row, column=3).value = activity
                worksheet.cell(row=last_row, column=4).value = time
                workbook.save(pm.filepathlog)
            else:
                print("Gagal write log data")
        except Exception as e:
            print("Gagal write log\nMesage Error : ", str(e))
