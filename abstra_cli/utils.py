import os
import json


def create_abstra_dir():
    path = rebase_path()
    if not os.path.exists(path):
        os.makedirs(path)


def rebase_path(path="/"):
    return os.path.expanduser("~/.abstra" + path)


def save_user_config(data):
    if isinstance(data, dict):
        data = json.dumps(data)
    create_abstra_dir()
    path = rebase_path("/user.json")
    with open(path, "w") as f:
        f.write(data)


def read_user_config():
    path = rebase_path("/user.json")
    with open(path) as f:
        return json.load(f)
