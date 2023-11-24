import streamlit as st
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
# ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
#ローカル
# credentials = Credentials.from_service_account_file("venv/my-project-20230927-1db60d7e8989.json", scopes=scope)
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
# 一行目をカラム名にする
df.columns = df.iloc[0]
# 一行目を削除する
df = df[1:]
st.title('Daily Log')
st.header("Let's self-reflect!")


with st.form("my_form", clear_on_submit=False):
    line_id = st.text_input('line_idを入力して下さい。')
    submitted = st.form_submit_button("日記を出力")

if submitted:
    df = df[df.iloc[:, 6] == line_id ]
    #降順ソートする
    df = df.sort_values(by=df.columns[0], ascending=False)
    #現在のカウントを取得
    new_count = df.iloc[0, 5]
    st.subheader(f"現在記録{new_count}日です。")
    df_list = df.values.tolist()
    # Streamlitで表示
    # st.title('Spreadsheet Data')
    # st.write(df)
    # 一列目を取得
    column_one = df.iloc[:, 0]

    # 重複を除去して新しいデータフレームを作成
    new_df = pd.DataFrame({df.columns[0]: column_one.unique()})

    # DataFrameをリストに変換
    new_df_list = new_df.values.tolist()
    view_df_list = []
    hoge1, hoge2, hoge3, hoge4 = ("", "", "", "")
    num = 0

    for j in df_list:
        ymd = new_df_list[num][0]
        if j[0] == ymd:
            if j[1] != "":
                hoge1 += j[1] +"  \n"
            if j[2] != "":
                hoge2 += j[2] +"  \n"
            if j[3] != "":
                hoge3 += j[3] +"  \n"
            if j[4] != "":
                hoge4 += j[4] +"  \n"
        else:
            view_df_list.append([ymd, hoge1, hoge2, hoge3, hoge4])
            hoge1, hoge2, hoge3, hoge4 = ("", "", "", "")
            num += 1
            ymd = new_df_list[num][0]
            if j[0] == ymd:
                if j[1] != "":
                    hoge1 += j[1] + "  \n"
                if j[2] != "":
                    hoge2 += j[2] + "  \n"
                if j[3] != "":
                    hoge3 += j[3] + "  \n"
                if j[4] != "":
                    hoge4 += j[4] + "  \n"
    view_df_list.append([ymd, hoge1, hoge2, hoge3, hoge4])
    # for view in view_df_list:
    #     print(view)
    viewer_df = pd.DataFrame(view_df_list,columns=["date","自己肯定感or効力感","明日必ずやる","今日の振り返り","今日の一言"])
    # print(viewer_df)




    # print(df_list)



    # # Streamlitで表示
    st.dataframe(viewer_df,hide_index=True,)
    # print(new_df_list)