import pandas as pd
import datetime
import json
import requests as req


def login() -> dict:
    """Melakukan login ke API sigadis dan mengembalikan headers untuk request selanjutnya"""
    url = "https://api.sigadispln.com/login"
    # username dan password sigadis
    body = {
        "username": "gadisbot",
        "password": "gadisbot"}
    r = req.post(url, json=body)
    token = r.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def post_data(nomor_gardu: str):
    # baca file hasil download
    df = pd.read_excel('data//source//Load Profile Detail.xlsx',
                       usecols=['Date', 'VR', 'VS', 'VT', 'IR', 'IS', 'IT', 'IN', 'PF Total'])

    # buat filter tanggal
    most_recent_date = datetime.datetime.date(
        df.Date.max())  # tanggal terbaru dari data
    most_recent_date = pd.Timestamp(most_recent_date)  # ubah ke timestamp

    # filter datanya, sehingga yang diambil adalah data dari tanggal terakhir mulai dari jam 00.00
    df = df[df.Date >= most_recent_date]

    # buat column baru untuk menampung tanggal dalam string
    df['tanggal'] = pd.DatetimeIndex(df.Date).strftime('%Y-%m-%d %H:%M:%S')

    # Get master dataframe

    # lookup nomor yang pake idpel dengan nomor gardu
    # jika idpel, maka ganti ke nomor gardu, cek jumlah digit
    sub_nomor_gardu = nomor_gardu[:2]
    if (sub_nomor_gardu != "GD"):
        # Ambil nomor gardunya
        nomor_gardu = get_gardu_by_idpel(nomor_gardu)
        df['nomor_gardu'] = nomor_gardu  # 'GD321111138'
        # rename nama kolum sesuai dengan yang diminta API
        df.rename(columns={'VR': 'vr', 'VS': 'vs', 'VT': 'vt', 'IR': 'i_r',
                           'IS': 'i_s', 'IT': 'i_t', 'IN': 'i_netral', 'PF Total': 'pf_total',
                           }, inplace=True)

        # pilih hanya beberapa kolom yang sesuai
        df_final = df[['nomor_gardu', 'tanggal', 'vr', 'vs',
                       'vt', 'i_r', 'i_s', 'i_t', 'i_netral', 'pf_total']]
        list_data = df_final.to_dict(orient='list')

        # API URL
        url = 'https://api.sigadispln.com/pengukuran'

        headers = login()

        # post data ke API
        r = req.post(url, headers=headers, json=list_data)
        print(r.status_code)
        print("Idpel bernomor gardu")
    else:
        df['nomor_gardu'] = nomor_gardu  # 'GD321111138'
        # rename nama kolum sesuai dengan yang diminta API
        df.rename(columns={'VR': 'vr', 'VS': 'vs', 'VT': 'vt', 'IR': 'i_r',
                           'IS': 'i_s', 'IT': 'i_t', 'IN': 'i_netral', 'PF Total': 'pf_total',
                           }, inplace=True)

        # pilih hanya beberapa kolom yang sesuai
        df_final = df[['nomor_gardu', 'tanggal', 'vr', 'vs',
                       'vt', 'i_r', 'i_s', 'i_t', 'i_netral', 'pf_total']]
        list_data = df_final.to_dict(orient='list')

        # API URL
        url = 'https://api.sigadispln.com/pengukuran'

        headers = login()

        # post data ke API
        r = req.post(url, headers=headers, json=list_data)
        print(r.status_code)


def get_gardu_by_idpel(idpel) -> str:
    url = 'https://api.sigadispln.com/gardu?no_meter=exist'
    headers = login()
    r = req.get(url, headers=headers)
    j = r.json()
    data = j['data']
    df = pd.DataFrame.from_dict(data)
    nomor_gardu = df['nomor_gardu'][df['idpel'] == idpel].to_list()[0]
    return nomor_gardu


def get_gardu() -> list[str]:
    url = 'https://api.sigadispln.com/gardu?no_meter=exist'
    headers = login()
    r = req.get(url, headers=headers)
    j = r.json()
    data = j['data']
    df = pd.DataFrame.from_dict(data)
    # buat dataFrame Gardu Khusus
    dfumum = df[df['tipe_gardu'] == "UMUM"]
    # buat dataFrame Gardu Khusus
    dfkhusus = df[df['tipe_gardu'] == "KHUSUS"]
    # add df khusus dan ummum ke datalist
    # list_gardu = df[df['nomor_meter'].notnull()]['nomor_gardu'].to_list()

    # add list khusus dengan idpel
    listkhusus = dfkhusus["idpel"]
    listumum = dfumum["nomor_gardu"]
    dflistgardu = pd.concat([listkhusus, listumum])
    list_gardu = dflistgardu.to_list()
    print(list_gardu, sep="\n")
    return list_gardu


# post_data('GD321111141')
