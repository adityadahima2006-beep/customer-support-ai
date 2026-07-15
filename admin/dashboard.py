import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import (
    get_total_users,
    get_total_chats,
    get_sentiment_counts,
    get_recent_chats,
    search_chats,
    get_all_chats
)


def show_dashboard():

    st.header("📊 Customer Support Analytics Dashboard")

    # ==========================
    # Analytics
    # ==========================

    total_users = get_total_users()
    total_chats = get_total_chats()

    positive, neutral, negative = get_sentiment_counts()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("👥 Users", total_users)
    col2.metric("💬 Chats", total_chats)
    col3.metric("😊 Positive", positive)
    col4.metric("😐 Neutral", neutral)
    col5.metric("😔 Negative", negative)

    st.markdown("---")

    # ==========================
    # Search
    # ==========================

    st.subheader("🔍 Search Conversations")

    keyword = st.text_input(
        "Search by Username or Message"
    )

    if keyword.strip():

        chats = search_chats(keyword)

        st.success(f"Found {len(chats)} result(s).")

    else:

        chats = get_recent_chats()

    st.markdown("---")

    # ==========================
    # Charts
    # ==========================

    chart_data = pd.DataFrame({
        "Sentiment": [
            "Positive",
            "Neutral",
            "Negative"
        ],
        "Count": [
            positive,
            neutral,
            negative
        ]
    })

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("📊 Sentiment Bar Chart")

        fig = px.bar(
            chart_data,
            x="Sentiment",
            y="Count",
            text="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        st.subheader("🥧 Sentiment Pie Chart")

        fig = px.pie(
            chart_data,
            names="Sentiment",
            values="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    # ==========================
    # Conversation Table
    # ==========================

    st.subheader("📝 Conversation Table")

    if chats:

        table = pd.DataFrame(
            chats,
            columns=[
                "Username",
                "User Message",
                "Bot Response",
                "Timestamp"
            ]
        )

        st.dataframe(
            table,
            use_container_width=True
        )

    else:

        st.warning("No conversations found.")

    st.markdown("---")

    # ==========================
    # Export CSV
    # ==========================

    st.subheader("📤 Export Chat History")

    all_chats = get_all_chats()

    if all_chats:

        export_df = pd.DataFrame(
            all_chats,
            columns=[
                "Username",
                "User Message",
                "Bot Response",
                "Timestamp"
            ]
        )

        csv = export_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name="chat_history.csv",
            mime="text/csv"
        )

    st.markdown("---")

    # ==========================
    # Conversation Details
    # ==========================

    st.subheader("📜 Conversation Details")

    for username, user_msg, bot_msg, timestamp in chats:

        with st.expander(
            f"👤 {username} | {timestamp}"
        ):

            st.write("### 👤 User")
            st.write(user_msg)

            st.write("### 🤖 Assistant")
            st.write(bot_msg)
