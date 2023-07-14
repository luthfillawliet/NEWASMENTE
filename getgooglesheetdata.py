import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe

GSHEETNAME = 'Monitoring TS P2TL 2023'
#TAB_NAME = 'REPORT HARIAN'
TAB_NAME = 'YOY'

def get_sheet_data(GSHEETNAME,TAB_NAME):
    gc = gspread.service_account(filename=R'data\gsheet\monitoringpju-290711-01d17333a9eb.json')
    sh = gc.open(GSHEETNAME)
    #print(sh.sheet1.get(TAB_NAME))
    worksheet = sh.worksheet(TAB_NAME)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

def write_df_to_sheet(GSHEET,TAB_NAME,df):
    #access the spreadsheet
    gc = gspread.service_account(filename=R'data\gsheet\monitoringpju-290711-01d17333a9eb.json')
    sh = gc.open(GSHEETNAME)
    worksheet = sh.worksheet(TAB_NAME)
    set_with_dataframe(worksheet=worksheet,dataframe=df)

df = get_sheet_data(GSHEETNAME=GSHEETNAME,TAB_NAME=TAB_NAME)
print(df)
high_ts = df[df["2023"]>=1200000]
print(high_ts)

#write data to google sheet
write_df_to_sheet(GSHEET=GSHEETNAME,TAB_NAME='TEST_PYTHON',df=high_ts)