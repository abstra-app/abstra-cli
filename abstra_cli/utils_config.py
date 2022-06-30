import os
import json

from .utils import create_abstra_dir
from .apis import get_workspace_from_token


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
    return os.getenv('ABSTRA_API_TOKEN') or read_config().get('api_token')


def get_auth_config():
    api_token = get_api_token()
    workspace_id = get_workspace_from_token(api_token)
    return api_token, workspace_id


def config_check(f):
    def wrapper(*args):
        if not get_api_token():
            raise Exception("No API token configured")
        return f(*args)
    return wrapper
