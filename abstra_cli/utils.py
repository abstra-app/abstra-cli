import os


def create_abstra_dir():
    path = rebase_path()
    if not os.path.exists(path):
        os.makedirs(path)


def rebase_path(path="/"):
    return os.path.expanduser("~/.abstra" + path)


def save_user_config(data):
    create_abstra_dir()
    path = rebase_path("/user.json")
    with open(path, "w") as f:
        f.write(data)
