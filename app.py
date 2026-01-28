import streamlit as st
import pandas as pd
import plotly.express as px

#ページ冒頭
st.title('ガソリンの値段推移')
st.markdown("### このアプリについて\n e-Statのデータを用いて、日本の各都市におけるガソリン価格の推移を可視化したものです。")

#データ読み込みと前処理
df = pd.read_csv('gas.csv')

#2025年12月 → 2025-12 (AIからのアドバイス)
df["month"] = pd.to_datetime(df["時間軸（月）"], format="%Y年%m月").dt.to_period("M")

col = st.columns(3)
#都市の選択
with st.sidebar:
    city = st.selectbox('都市を選択してください',
                              df.columns[4::])
    compare = st.multiselect("比較したい都市を選択してください(複数可)",
                             df.columns[4::],
                             default=['札幌市', '那覇市'])
#年の選択(スライダー)
min_year = int(df["month"].dt.year.min())
max_year = int(df["month"].dt.year.max())
year = col[0].slider(label='年を選択してください',
                      min_value=min_year,
                      max_value=max_year,
                      value=df["month"].dt.year.min())


#年データの整形
df_year = df[df["month"].dt.year == year].copy()
df_year["month_str"] = df_year["month"].astype(str)
df_year[city] = pd.to_numeric(df_year[city], errors="coerce")

#全期間データ
df_all = df.copy()
df_all["month_str"] = df_all["month"].astype(str)
df_all[city] = pd.to_numeric(df_all[city], errors="coerce")

#前年差(①未使用UI:metric)
avg_price = df_year[city].mean()
max_price = df_year[city].max()
divide = max_price - avg_price
col[2].metric(label=f"{year}年の最高価格", value=f"{max_price:.1f}円", delta=f"+{divide:.1f}円")

#グラフ1
fig1 = px.bar(df_year,
             x="month_str",
             y=city,
             title=f"{city}の{year}年 月別ガソリン価格",
             labels={"month_str": "年月", city: "価格(円)"})
st.plotly_chart(fig1) 

#グラフ2
if compare:
    st.subheader(f"全期間の価格推移({min_year}年~{max_year}年)")
    fig2 = px.line(df_all,
                x="month_str",
                y=compare,
                title="選択した都市のガソリン価格推移比較",
                labels={"month_str":"年月",city: "価格(円)", "variable":"都市名"})
    st.plotly_chart(fig2)
else:
    st.warning("サイドバーで比較したい都市を1つ以上選んでください。")

##分析・解釈コメント(②未使用UI:info)
st.subheader("傾向の分析")
st.info(f"""
        このグラフから、{city}におけるガソリン価格の変動を確認できます。\n特に{year}年の最高値は{max_price}でした。
        """)

# expander (③未使用UI:expander)
with st.expander("詳細なデータを見る(元データ)"):
    st.write("出典: e-Stat 小売物価統計調査")
    st.dataframe(df)

