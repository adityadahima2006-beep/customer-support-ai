import json
import os
import streamlit as st

USER_DB = "database/users.json"


def register_user():
    """
    Display registration form and create a new user.
    """

    username = st.text_input("Choose Username")

    password = st.text_input(
        "Choose Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        if not username or not password or not confirm_password:

            st.error("Please fill in all fields.")
            return

        if password != confirm_password:

            st.error("Passwords do not match.")
            return

        if os.path.exists(USER_DB):

            try:
                with open(USER_DB, "r") as file:
                    users = json.load(file)
            except Exception:
                users = {}

        else:
            users = {}

        if username in users:

            st.error("Username already exists.")
            return

        users[username] = password

        with open(USER_DB, "w") as file:
            json.dump(users, file, indent=4)

        st.success("Registration Successful! Please login.")
