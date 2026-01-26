import streamlit as st
import pandas as pd
import plotly.express as px

st.title('睡眠時間の推移')

df = pd.read_csv('data_2021.csv', encoding='cp932')

st.header('睡眠時間の推移について知ることができます。')

df = df.rename(columns={
    "01_睡眠" : "sleep",
    "年齢" : "age",
    "男女" : "sex",
    "曜日" : "day",
})

df['sleep'] = pd.to_numeric(df['sleep'], errors='coerce')

df = df[["sleep", "age", "sex", "day"]]

with st.sidebar: 
    age = st.number_input("あなたの年齢を入力してください",
                          min_value=15,
                          max_value=120,
                          value=40,
                          step=1)
    
    theme = st.selectbox("テーマを選択してください",
                     ["年齢", "性別", "曜日",])
    
    if theme == "年齢":
        col = 'age'
    
    elif theme == "性別":
        col = 'sex'
    
    elif theme == "曜日":
        col = 'day'

fig = px.bar(df.reset_index(),
             x=col,
             y="sleep",
             color=col,
             title=f"{theme}ごとの睡眠時間比較")
st.plotly_chart(fig)
    

