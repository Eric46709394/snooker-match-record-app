import streamlit as st
import pandas as pd

st.set_page_config(page_title="Snooker Match Record")

st.title("Snooker Match Record")

# 初始化狀態
if "players" not in st.session_state:
    st.session_state.players = []
if "records" not in st.session_state:
    st.session_state.records = []

# 側邊：步驟一／玩家設定
with st.sidebar:
    st.header("Step 1: 玩家設定")
    num = st.number_input("玩家人數", min_value=2, step=1, key="num_players")
    if st.button("確定玩家數"):
        st.session_state.players = []
        for i in range(num):
            name = st.text_input(f"玩家 {i+1} 名稱", key=f"player_{i}")
            st.session_state.players.append(name)
    if st.session_state.players:
        st.write("目前玩家：", st.session_state.players)

# 主區：步驟二／輸入比賽紀錄
st.header("Step 2: 輸入比賽資料")
if st.session_state.players:
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.selectbox("玩家 1", st.session_state.players, key="p1")
        s1 = st.number_input("玩家 1 得分", min_value=0, key="s1")
    with col2:
        p2 = st.selectbox("玩家 2", st.session_state.players, key="p2")
        s2 = st.number_input("玩家 2 得分", min_value=0, key="s2")

    highest_break = st.number_input("本局最高一桿分數", min_value=0, key="break_score")
    breaker = st.selectbox("打出最高一桿的玩家", [p1, p2], key="breaker")

    if st.button("新增比賽紀錄"):
        if p1 == p2:
            st.error("玩家 1 和玩家 2 不能是同一人")
        else:
            st.session_state.records.append({
                "玩家1": p1,
                "分數1": s1,
                "玩家2": p2,
                "分數2": s2,
                "最高一桿": highest_break,
                "打出者": breaker
            })

# 步驟三／統計與排名
st.header("Step 3: 統計結果與排名")
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)

    stats = {p: {"勝場": 0, "最高入球": 0, "最高一桿": 0} for p in st.session_state.players}
    for rec in st.session_state.records:
        p1, p2, s1v, s2v = rec["玩家1"], rec["玩家2"], rec["分數1"], rec["分數2"]
        stats[p1]["最高入球"] = max(stats[p1]["最高入球"], s1v)
        stats[p2]["最高入球"] = max(stats[p2]["最高入球"], s2v)
        if s1v > s2v:
            stats[p1]["勝場"] += 1
        elif s2v > s1v:
            stats[p2]["勝場"] += 1
        br = rec["最高一桿"]
        stats[rec["打出者"]]["最高一桿"] = max(stats[rec["打出者"]]["最高一桿"], br)

    ranking = pd.DataFrame([{"玩家": p, **stats[p]} for p in stats])
    ranking = ranking.sort_values(by=["勝場", "最高入球"], ascending=False)
    ranking.index += 1

    st.table(ranking)
    st.subheader("每局對戰紀錄")
    st.dataframe(df)

    to_download = pd.concat([ranking, df], sort=False)
    st.download_button("📥 下載 CSV 匯總", to_download.to_csv(index=False), "snooker_record.csv", "text/csv")