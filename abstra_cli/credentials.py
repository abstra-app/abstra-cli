import os
from abstra_cli.utils import ABSTRA_FOLDER, CREDENTIALS_FILE


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
