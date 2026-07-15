import streamlit as st

from database.db import create_tables
from auth.auth_signup import register_user
from auth.auth_login import login_user
from auth.auth_session import initialize_session, login, logout
from chatbot.chat_interface import show_chat
from admin.dashboard import show_dashboard

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Customer Support AI",
    page_icon="🤖",
    layout="wide"
)

create_tables()
initialize_session()

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:

    st.title("🤖 Customer Support AI")

    if st.session_state.logged_in:

        st.success(f"Logged in as: {st.session_state.username}")

        page = st.radio(
            "Navigation",
            [
                "💬 Chat",
                "📊 Admin Dashboard"
            ]
        )

        st.markdown("---")

        if st.button("🚪 Logout"):
            logout()
            st.rerun()

# -------------------------------
# Login / Register
# -------------------------------
if not st.session_state.logged_in:

    st.title("🤖 Customer Support Multi-Agent AI")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    # Login
    with tab1:

        st.subheader("Login")

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            success, message = login_user(
                login_username,
                login_password
            )

            if success:
                login(login_username)
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    # Register
    with tab2:

        st.subheader("Register")

        register_username = st.text_input(
            "Choose Username",
            key="register_username"
        )

        register_password = st.text_input(
            "Choose Password",
            type="password",
            key="register_password"
        )

        if st.button("Create Account"):

            success, message = register_user(
                register_username,
                register_password
            )

            if success:
                st.success(message)
            else:
                st.error(message)

# -------------------------------
# Main Application
# -------------------------------
else:

    if page == "💬 Chat":

        st.title("🤖 Customer Support AI")

        st.success(
            f"Welcome {st.session_state.username}!"
        )

        st.info(
            "✅ Login Successful.\n\n"
            "Customer Support AI is ready."
        )

        st.markdown("---")

        show_chat()

    elif page == "📊 Admin Dashboard":

        st.title("📊 Customer Support Analytics")

        show_dashboard()


# ----------------------------------
# Footer
# ----------------------------------
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; font-size:16px; color:gray;">
        Developed by <b>Aditya Kumar Dahima</b>
    </div>
    """,
    unsafe_allow_html=True
)