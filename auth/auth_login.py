import json
import os

USER_DB = "database/users.json"


def login_user(username, password):

    if not username or not password:
        return False, "Please enter both username and password."

    if not os.path.exists(USER_DB):
        return False, "No users found. Please register first."

    with open(USER_DB, "r") as file:
        users = json.load(file)

    if username not in users:
        return False, "Username does not exist."

    if users[username] != password:
        return False, "Incorrect password."

    return True, "Login Successful!"
