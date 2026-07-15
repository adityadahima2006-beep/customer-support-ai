import streamlit as st


def initialize_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = None


def login(username):
    st.session_state.logged_in = True
    st.session_state.username = username


def logout():
    st.session_state.logged_in = False
    st.session_state.username = None