import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    # 1년간 박스오피스 10위권에 든 영화 216편의 요약표를 불러옵니다
    df = pd.read_csv(DATA_URL)
    # 장르가 세로막대 기호(|)로 여러 개 적힌 영화는 첫 번째 장르만 씁니다
    df["장르"] = df["genre"].str.split("|").str[0]
    return df


df = load_data()

# ── 그래프 1. 장르별 영화 편수 도넛 ──
st.header("1. 장르별 영화 편수 (도넛)")
genre_count = df["장르"].value_counts().reset_index()
genre_count.columns = ["장르", "편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.45,  # 가운데 구멍을 뚫어 도넛 모양으로
)
fig.update_traces(hovertemplate="%{label}<br>%{value}편 (%{percent})<extra></extra>")
st.plotly_chart(fig, width="stretch")

st.text_input("이 그래프로 알 수 있는 것", key="note1")

st.divider()

# ── 그래프 2. 장르 안의 영화 트리맵 ──
st.header("2. 장르 안 영화별 총 관객수 (트리맵)")

fig2 = px.treemap(
    df,
    path=["장르", "movieNm"],
    values="total_audi",
)
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,}명<extra></extra>"
)
st.plotly_chart(fig2, width="stretch")

st.text_input("이 그래프로 알 수 있는 것", key="note2")

st.divider()

# ── 그래프 3. 총 관객수 히스토그램 ──
st.header("3. 총 관객수 분포 (히스토그램)")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
)
fig3.update_traces(hovertemplate="관객 %{x}<br>영화 수: %{y}편<extra></extra>")
fig3.update_layout(xaxis_title="총 관객수", yaxis_title="영화 편수")
st.plotly_chart(fig3, width="stretch")

counts, bin_edges = np.histogram(df["total_audi"], bins=30)
max_bin_idx = counts.argmax()
bin_start = int(bin_edges[max_bin_idx])
bin_end = int(bin_edges[max_bin_idx + 1])

top_movie = df.loc[df["total_audi"].idxmax()]

st.markdown(
    f"- 대부분의 영화(**{counts.max()}편**)는 총 관객 **{bin_start:,}명 ~ {bin_end:,}명** 구간에 몰려 있습니다.\n"
    f"- 가장 관객이 많은 영화는 **{top_movie['movieNm']}**이며, 총 **{int(top_movie['total_audi']):,}명**을 동원했습니다."
)

st.text_input("이 그래프로 알 수 있는 것", key="note3")

st.divider()

# ── 그래프 4. 개봉일 스크린수 vs 총 관객수 산점도 ──
st.header("4. 개봉일 스크린수와 총 관객수의 관계 (산점도)")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="장르",
    hover_name="movieNm",
)
fig4.update_layout(xaxis_title="개봉일 스크린수", yaxis_title="총 관객수")
st.plotly_chart(fig4, width="stretch")

st.text_input("이 그래프로 알 수 있는 것", key="note4")

st.divider()

# ── 그래프 5. 장르별 총 관객수 박스플롯 (10편 이상 장르만) ──
st.header("5. 장르별 총 관객수 분포 (박스플롯)")

genre_counts_all = df["장르"].value_counts()
major_genres = genre_counts_all[genre_counts_all >= 10].index
df_major = df[df["장르"].isin(major_genres)]

fig5 = px.box(
    df_major,
    x="장르",
    y="total_audi",
    hover_name="movieNm",
)
fig5.update_traces(boxpoints="outliers")
fig5.update_layout(xaxis_title="장르", yaxis_title="총 관객수")
st.plotly_chart(fig5, width="stretch")

st.text_input("이 그래프로 알 수 있는 것", key="note5")

st.divider()

# ── 그래프 6. 개봉일 스크린수 vs 총 관객수 버블 그래프 (점 크기 = 첫 주 관객) ──
st.header("6. 개봉일 스크린수와 총 관객수의 관계 (버블)")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="장르",
    hover_name="movieNm",
    size_max=40,
)
fig6.update_layout(xaxis_title="개봉일 스크린수", yaxis_title="총 관객수")
st.plotly_chart(fig6, width="stretch")

st.text_input("이 그래프로 알 수 있는 것", key="note6")

st.divider()

# ── 그래프 7. 국가 → 장르 선버스트 (칸 크기 = 영화 편수) ──
st.header("7. 제작 국가별 장르 구성 (선버스트)")

fig7 = px.sunburst(
    df,
    path=["nation", "장르"],
)
fig7.update_traces(hovertemplate="<b>%{label}</b><br>%{value}편<extra></extra>")
st.plotly_chart(fig7, width="stretch")

st.text_input("이 그래프로 알 수 있는 것", key="note7")

st.divider()
st.header("8. (다음 그래프를 여기에 추가)")
