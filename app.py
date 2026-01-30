import streamlit as st
import pandas as pd
import plotly.express as px

#ページ冒頭
st.title('ガソリンの値段推移')
st.markdown("---")
st.markdown("### このアプリについて\n e-Statのデータを用いて、日本の各都市におけるガソリン価格の推移を可視化したものです。")
st.markdown("---")
st.subheader("都市別年間ガソリン価格の推移")

#データ読み込みと前処理
df = pd.read_csv('gas.csv')

#使用した表に欠測が存在するため errors="coerce"を用いてNaNに変換する
for col_name in df.columns[4:]:
    df[col_name] = pd.to_numeric(df[col_name], errors="coerce")

#データ処理用の年月情報(period型に変換)
df["month"] = pd.to_datetime(df["時間軸（月）"], format="%Y年%m月").dt.to_period("M")

#表示用(astypeでstr型に変換)
df["month_str"] = df["month"].astype(str)

cols=st.columns([1, 3])
top_left_container = cols[0].container(border=True)
bottom_left_container=cols[0].container(border=True)

#都市の選択
with top_left_container:
    city = st.selectbox('都市を選択してください',
                              df.columns[4::])
    
    min_year = int(df["month"].dt.year.min())
    max_year = int(df["month"].dt.year.max())

    year = st.slider(label='年を選択してください',
                      min_value=min_year,
                      max_value=max_year,
                      value=df["month"].dt.year.min())


#ブールインデックスを用いて選択した年のデータだけを df_yearに格納
#.copy()で元データを破壊せずに中身をいじれる
df_year = df[df["month"].dt.year == year].copy()
df_all = df.copy()
current_price = df_year[city].mean()

#前年のデータを取得して平均価格を計算
pre_year = year - 1
df_pre = df[df["month"].dt.year == pre_year]

#前年のデータが存在すれば選択年との差額および割合を計算
with bottom_left_container:
    if not df_pre.empty:
        pre_price = df_pre[city].mean()

        diff_price = current_price - pre_price
        ratio = (diff_price / pre_price) * 100

        #未使用UI1(metric)
        st.metric(label=f"{city}の{year}年 平均価格",
                  value=f"{current_price:.1f}円",
                  delta=f"{diff_price:+.1f}円({ratio:+.1f}%)",)
    else:
        st.metric(label=f"{city}の{year}年 平均価格",
                  value=f"{current_price:.1f}",
                  delta=None)

y_min = df_year[city].min() - 5
y_max = df_year[city].max()

right_container = cols[1].container(border=True)
       
#グラフ1
with right_container:
    fig1 = px.bar(df_year,
                x="month_str",
                y=city,
                title=f"{city}の{year}年 月別ガソリン価格",
                labels={"month_str": "年月", city: "価格(円)"})
    fig1.update_yaxes(range=[y_min, y_max])
    st.plotly_chart(fig1, use_container_width=True) # グラフの幅を動的に変える

min_price = df_year[city].min()
max_price = df_year[city].max()

#未使用UI2(info)
st.info(f"""
        傾向の分析\n
        このグラフから、{city}におけるガソリン価格の変動を確認できます。
        {year}年の最高値は{max_price}円、最低値は{min_price}円でした。
        下のグラフでほかの都市と比較してみましょう。
        """)

st.markdown("---")

st.subheader(f"全期間の価格推移比較({min_year}年~{max_year}年)")

compare = st.multiselect("比較したい都市を選択してください(複数可)",
                            df.columns[4::],
                            default=['札幌市', '那覇市'])

#グラフ2
if compare:
    fig2 = px.line(df_all,
                x="month_str",
                y=compare,
                title="選択した都市のガソリン価格推移比較",
                labels={"month_str":"年月",city: "価格(円)", "variable":"都市名"})
    st.plotly_chart(fig2, use_container_width=True) #グラフの幅を動的に変える
else:
    st.warning("比較したい都市を1つ以上選んでください。")

# expander (③未使用UI:expander)
with st.expander("生データを見る"):
    st.write("出典: e-Stat 小売物価統計調査")
    st.dataframe(df)

