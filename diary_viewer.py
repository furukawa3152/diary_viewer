import streamlit as st
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
# ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
credentials = Credentials.from_service_account_file("my-project-20230927-1db60d7e8989.json", scopes=scope)

gc = gspread.authorize(credentials)

# スプレッドシートIDを変数に格納する。
SPREADSHEET_KEY = os.environ["SPREADSHEET_KEY"]
# スプレッドシート（ブック）を開く
workbook = gc.open_by_key(SPREADSHEET_KEY)

# シートの一覧を取得する。（リスト形式）
worksheets = workbook.worksheets()
# シートを開く
sheet = workbook.worksheet('シート1')
data = sheet.get_all_values()
# Pandas DataFrameに変換
df = pd.DataFrame(data)
#
# Streamlitで表示
st.title('Spreadsheet Data')
st.write(df)
