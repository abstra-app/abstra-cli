import os
import json

from .utils import create_abstra_dir


def save_config(data):
    if isinstance(data, dict):
        data = json.dumps(data)
    path = create_abstra_dir() + "/config.json"
    with open(path, "w") as f:
        f.write(data)


def read_config():
    path = create_abstra_dir() + "/config.json"

    if not os.path.exists(path):
        return {}

    with open(path) as f:
        return json.load(f)


def get_api_token():
    return os.getenv('ABSTRA_API_TOKEN') or read_config()['api_token']


def config_check(f):
    def wrapper(*args):
        if not get_api_token():
            return print("Please configure the CLI first")
        return f(*args)
    return wrapper
