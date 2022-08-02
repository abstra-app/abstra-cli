import os

from .public_apis import get_workspace_from_token

ABSTRA_FOLDER = ".abstra"
CREDENTIALS_FILE = ".abstra/credentials"


def create_abstra_dir():
    if not os.path.exists(ABSTRA_FOLDER):
        os.makedirs(ABSTRA_FOLDER)


def save_credentials(api_token: str):
    create_abstra_dir()
    with open(CREDENTIALS_FILE, "w") as f:
        f.write(api_token.strip())


def get_credentials():
    if os.getenv("ABSTRA_API_TOKEN"):
        return os.getenv("ABSTRA_API_TOKEN")

    if not os.path.exists(CREDENTIALS_FILE):
        return None

    with open(CREDENTIALS_FILE) as f:
        return f.read().strip()


def get_auth_info():
    api_token = get_credentials()
    if not api_token:
        return None, None
    workspace_id = get_workspace_from_token(api_token)
    return api_token, workspace_id


def credentials_check(f):
    def wrapper(*args, **kwargs):
        api_token, workspace_id = get_auth_info()
        if not api_token:
            raise Exception("No API token configured")
        if not workspace_id:
            raise Exception("Bad token: no workspace found")
        return f(*args, **kwargs)

    return wrapper
