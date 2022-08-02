import os
import json

from .utils import rebase_path
from .apis import get_workspace_from_token

ABSTRA_FOLDER = "./abstra"
CONFIG_FILE = "/config.json"


def create_abstra_dir():
    path = rebase_path(ABSTRA_FOLDER)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def config_file_path():
    return create_abstra_dir() + CONFIG_FILE


def save_config(data):
    if isinstance(data, dict):
        data = json.dumps(data)
    with open(config_file_path(), "w") as f:
        f.write(data)


def get_config():
    path = config_file_path()

    if not os.path.exists(path):
        return {}

    with open(path) as f:
        return json.load(f)


def get_api_token():
    return os.getenv("ABSTRA_API_TOKEN") or get_config().get("api_token")


def save_api_token(api_token):
    save_config({"api_token": api_token})


def get_auth_config():
    api_token = get_api_token()
    if not api_token:
        return None, None
    workspace_id = get_workspace_from_token(api_token)
    return api_token, workspace_id


def token_check(f):
    def wrapper(*args):
        if not get_api_token():
            raise Exception("No API token configured")
        return f(*args)

    return wrapper
