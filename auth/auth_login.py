import json
import os
import streamlit as st

USER_DB = "database/users.json"


def login_user():
    """
    Display login form and authenticate user.

    Returns:
        (username, password) on successful login
        (None, None) otherwise
    """

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if not username or not password:

            st.error("Please enter both username and password.")

            return None, None

        if not os.path.exists(USER_DB):

            st.error("No users found. Please register first.")

            return None, None

        try:

            with open(USER_DB, "r") as file:

                users = json.load(file)

        except Exception:

            st.error("Unable to read user database.")

            return None, None

        if username not in users:

            st.error("Username does not exist.")

            return None, None

        if users[username] != password:

            st.error("Incorrect password.")

            return None, None

        return username, password

    return None, None
