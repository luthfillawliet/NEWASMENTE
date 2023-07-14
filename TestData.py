import pandas as pd
import openpyxl
import xlwt
import datetime
import parameter
import numpy as np

#import gspreadsheet



pm = parameter.Parameter()
namafiletagsus =  pm.download_ts+"//"+pm.namafiletagsus
skiprows = 8
# try:
#     df = pd.read_excel(io=namafiletagsus,sheet_name="Report1",skiprows=skiprows)
#     print("Success")
# except:
#     print("gagal")

# print(df.loc[:,'2'])

# Get the current date and time
current_date = datetime.datetime.now()

# Extract the month from the current date
current_month = current_date.month

# Print the current month
print(current_month)
months = np.array(['1.Januari', '2.Februari', '3.Maret', '4.April', '5.Mei', '6.Juni', '7.Juli',
                   '8.Agustus', '9.September', '10.Oktober', '11.November', '12.Desember'])

month_number = 7  # Example value

# Access the corresponding month using the index
selected_month = months[month_number - 1]
print(selected_month)