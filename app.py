import streamlit as st
import pandas as pd
import plotly.express as px

st.title('ガソリンの値段推移')

df = pd.read_csv('gas.csv',)

#2025年12月 → 2025-12 (AIからのアドバイス)
df["month"] = pd.to_datetime(df["時間軸（月）"], format="%Y年%m月").dt.to_period("M")

with st.sidebar:
    prefecture = st.selectbox('都市を選択してください',
                              df.columns[4::])
    
    year = st.selectbox('年を入力してください',
                        df["month"].dt.year.unique())
    
    

