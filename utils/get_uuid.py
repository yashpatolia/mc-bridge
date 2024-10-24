import requests
import json
import logging


def get_uuid(username):
    with open('users.json', 'r') as file:
        users = json.load(file)

    if username.lower() in users['users'].values():
        uuid = list(users['users'].keys())[list(users['users'].values()).index(username.lower())]
    else:
        uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()['id']
        logging.info(f"GET https://api.mojang.com/users/profiles/minecraft/{username}")
        users['users'][uuid] = username.lower()
        with open('users.json', 'w') as file:
            file.write(json.dumps(users, indent=4))

    return uuid
