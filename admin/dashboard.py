import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

DB_PATH = "database/chat_history.db"


def show_dashboard():
    st.title("📊 Customer Support AI Dashboard")

    # Check database
    if not os.path.exists(DB_PATH):
        st.error("Database not found!")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM chat_history", conn)
        conn.close()
    except Exception as e:
        st.error(f"Database Error: {e}")
        return

    if df.empty:
        st.warning("No chat history available.")
        return

    # Create timestamp if missing
    if "timestamp" not in df.columns:
        df["timestamp"] = pd.date_range(
            end=pd.Timestamp.now(),
            periods=len(df),
            freq="min"
        )

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Message length
    df["Message Length"] = (
        df["user_message"]
        .astype(str)
        .str.len()
    )

    # ---------------- KPI ----------------

    st.subheader("📈 Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💬 Total Chats", len(df))
    col2.metric("👤 Users", df["username"].nunique())
    col3.metric("📝 Messages", len(df))
    col4.metric(
        "📏 Avg Length",
        int(df["Message Length"].mean())
    )

    st.divider()

    # ---------------- Charts Row 1 ----------------

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("👤 Chats Per User")

        user_counts = (
            df["username"]
            .value_counts()
            .reset_index()
        )

        user_counts.columns = ["Username", "Chats"]

        fig = px.bar(
            user_counts,
            x="Username",
            y="Chats",
            text="Chats",
            color="Chats"
        )

        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🥧 User Distribution")

        fig = px.pie(
            user_counts,
            names="Username",
            values="Chats",
            hole=0.45
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- Line Chart ----------------

    st.subheader("📈 Message Length")

    fig = px.line(
        df,
        x=df.index,
        y="Message Length",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- Timeline ----------------

    st.subheader("📅 Chat Timeline")

    timeline = (
        df.groupby(df["timestamp"].dt.date)
        .size()
        .reset_index(name="Chats")
    )

    timeline.columns = ["Date", "Chats"]

    fig = px.area(
        timeline,
        x="Date",
        y="Chats"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- Histogram ----------------

    st.subheader("📊 Message Length Distribution")

    fig = px.histogram(
        df,
        x="Message Length",
        nbins=15
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------------- Search ----------------

    st.subheader("🔍 Search Chats")

    search = st.text_input("Search by Username or Message")

    if search:
        filtered = df[
            df["username"].str.contains(search, case=False, na=False)
            |
            df["user_message"].str.contains(search, case=False, na=False)
        ]
        st.dataframe(filtered, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

    st.divider()

    # ---------------- Download ----------------

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Chat History",
        data=csv,
        file_name="chat_history.csv",
        mime="text/csv"
    )
