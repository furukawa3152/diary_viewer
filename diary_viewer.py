import streamlit as st
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
# ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
#ローカル
# credentials = Credentials.from_service_account_file("my-project-20230927-1db60d7e8989.json", scopes=scope)
#デプロイ用
credentials = Credentials.from_service_account_info( st.secrets["gcp_service_account"], scopes=[ "https://www.googleapis.com/auth/spreadsheets", ],)
gc = gspread.authorize(credentials)

# スプレッドシートIDを変数に格納する。
SPREADSHEET_KEY = st.secrets["SPREADSHEET_KEY"]
# SPREADSHEET_KEY = "1L65r8Dx8GZpn2qMyCU3V7hg2rZqfFZGMWcOm3j6qJ-0"
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
