import json
import os

USER_DB = "database/users.json"


def register_user(username, password):

    if not username or not password:
        return False, "Username and Password cannot be empty."

    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as file:
            users = json.load(file)
    else:
        users = {}

    if username in users:
        return False, "Username already exists."

    users[username] = password

    with open(USER_DB, "w") as file:
        json.dump(users, file, indent=4)

    return True, "Registration Successful!"
