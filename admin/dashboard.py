import streamlit as st
import sqlite3
import pandas as pd
import os


DB_PATH = "database/chat_history.db"


def show_dashboard():
    st.title("📊 Admin Dashboard")

    if not os.path.exists(DB_PATH):
        st.warning("Database not found.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)

        # -----------------------------
        # Load Chat History
        # -----------------------------
        try:
            df = pd.read_sql_query(
                "SELECT * FROM chat_history",
                conn
            )
        except Exception:
            st.info("No chat history found.")
            conn.close()
            return

        if df.empty:
            st.info("No chat records available.")
            conn.close()
            return

        # -----------------------------
        # Metrics
        # -----------------------------
        st.subheader("📈 Dashboard Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Chats", len(df))

        with col2:
            if "username" in df.columns:
                st.metric("Users", df["username"].nunique())
            else:
                st.metric("Users", 0)

        with col3:
            if "intent" in df.columns:
                st.metric("Intents", df["intent"].nunique())
            else:
                st.metric("Intents", 0)

        st.divider()

        # -----------------------------
        # Chat Records
        # -----------------------------
        st.subheader("💬 Chat History")

        st.dataframe(
            df,
            use_container_width=True
        )

        # -----------------------------
        # Intent Distribution
        # -----------------------------
        if "intent" in df.columns:

            st.subheader("📊 Intent Distribution")

            intent_counts = df["intent"].value_counts()

            st.bar_chart(intent_counts)

        # -----------------------------
        # Sentiment Distribution
        # -----------------------------
        if "sentiment" in df.columns:

            st.subheader("😊 Sentiment Distribution")

            sentiment_counts = df["sentiment"].value_counts()

            st.bar_chart(sentiment_counts)

        conn.close()

    except Exception as e:
        st.error(f"Dashboard Error: {e}")
