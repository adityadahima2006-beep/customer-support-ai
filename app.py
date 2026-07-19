import streamlit as st

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Customer Support AI",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Import Project Modules
# -------------------------------
try:
    from database.db import create_tables

    from auth.auth_signup import register_user
    from auth.auth_login import login_user
    from auth.auth_session import (
        initialize_session,
        login,
        logout
    )

    from chatbot.chat_interface import show_chat

    from admin.dashboard import show_dashboard

except Exception as e:
    st.error("Application import error:")
    st.exception(e)
    st.stop()


# -------------------------------
# Database Initialization
# -------------------------------
try:
    create_tables()

except Exception as e:
    st.error("Database initialization failed:")
    st.exception(e)
    st.stop()


# -------------------------------
# Session Initialization
# -------------------------------
initialize_session()


# -------------------------------
# Sidebar Navigation
# -------------------------------
def sidebar_menu():

    st.sidebar.title("🤖 Customer Support AI")

    if st.session_state.get("logged_in"):

        st.sidebar.success(
            f"Welcome, {st.session_state.get('username','User')}"
        )

        choice = st.sidebar.radio(
            "Navigation",
            [
                "Chat Assistant",
                "Admin Dashboard",
                "Logout"
            ]
        )

    else:

        choice = st.sidebar.radio(
            "Navigation",
            [
                "Login",
                "Register"
            ]
        )

    # -------------------------------
    # Developer Name
    # -------------------------------
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='text-align:center; color:gray;'><b>Developed by Aditya Kumar Dahima</b></div>",
        unsafe_allow_html=True
    )

    return choice


# -------------------------------
# Main Application
# -------------------------------
def main():

    choice = sidebar_menu()

    # ---------------------------
    # Register
    # ---------------------------
    if choice == "Register":

        st.title("📝 Create Account")

        register_user()

    # ---------------------------
    # Login
    # ---------------------------
    elif choice == "Login":

        st.title("🔐 Login")

        username, password = login_user()

        if username:

            login(username)

            st.success(
                "Login successful!"
            )

            st.rerun()


    # ---------------------------
    # Chat
    # ---------------------------
    elif choice == "Chat Assistant":

        if st.session_state.get("logged_in"):

            show_chat()

        else:

            st.warning(
                "Please login first."
            )


    # ---------------------------
    # Admin Dashboard
    # ---------------------------
    elif choice == "Admin Dashboard":

        if st.session_state.get("logged_in"):

            show_dashboard()

        else:

            st.warning(
                "Please login first."
            )


    # ---------------------------
    # Logout
    # ---------------------------
    elif choice == "Logout":

        logout()

        st.success(
            "Logged out successfully"
        )

        st.rerun()


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    main()

