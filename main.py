import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 날짜 열(하이픈 없는 여덟 자리 숫자)을 진짜 날짜형으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
    return df


df = load_data()

st.markdown(
    """
데이터 출처: [KOBIS 일별 박스오피스](https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv)  
하루 박스오피스 10위권 안에 든 영화들의 1년치(365일) 기록입니다.
"""
)

st.divider()

# ==============================================================
# 구역 1. 영화별 일별 관객수 변화
# ==============================================================
st.header("그래프 1. 영화별 일별 관객수 변화")

movie_list = sorted(df["영화명"].dropna().unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="movie_select_1")

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 일별 관객수 변화",
    labels={"날짜": "날짜", "일관객": "일일 관객수"},
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일일 관객수: %{y:,}명<extra></extra>"
)
fig1.update_layout(hovermode="x unified")

st.plotly_chart(fig1, use_container_width=True)

st.caption("💡 이 그래프로 알 수 있는 것: *(여기에 한 문장으로 적어보세요.)*")

st.divider()

# ==============================================================
# 구역 2. 일관객 합계 상위 5편의 날짜별 변화 비교
# ==============================================================
st.header("그래프 2. 일관객 합계 상위 5편 비교")

top5_titles = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index
)
top5_df = df[df["영화명"].isin(top5_titles)].sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일일 관객수",
    labels={"날짜": "날짜", "일관객": "일일 관객수", "영화명": "영화"},
)
fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일일 관객수: %{y:,}명<extra>%{fullData.name}</extra>"
)
fig2.update_layout(hovermode="x unified", legend_title_text="영화 (클릭하여 켜고 끄기)")

st.plotly_chart(fig2, use_container_width=True)

st.caption("💡 이 그래프로 알 수 있는 것: *(여기에 한 문장으로 적어보세요.)*")

st.divider()

# ==============================================================
# 구역 3. 날짜별 10위권 일관객 합계
# ==============================================================
st.header("그래프 3. 날짜별 10위권 일관객 합계")

daily_total = df.groupby("날짜")["일관객"].sum().reset_index()
daily_total.columns = ["날짜", "합계관객"]

top3_days = daily_total.sort_values("합계관객", ascending=False).head(3)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="합계관객",
    title="날짜별 10위권 일일 관객수 합계",
    labels={"날짜": "날짜", "합계관객": "일일 관객수 합계"},
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객수: %{y:,}명<extra></extra>"
)

for _, row in top3_days.iterrows():
    fig3.add_scatter(
        x=[row["날짜"]],
        y=[row["합계관객"]],
        mode="markers+text",
        marker=dict(size=10, color="red"),
        text=[row["날짜"].strftime("%Y-%m-%d")],
        textposition="top center",
        showlegend=False,
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객수: %{y:,}명<extra>상위 3일</extra>",
    )

st.plotly_chart(fig3, use_container_width=True)

st.caption("💡 이 그래프로 알 수 있는 것: *(여기에 한 문장으로 적어보세요.)*")
