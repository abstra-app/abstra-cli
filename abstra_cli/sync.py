from abstra_cli.auth import refresh_config
from .utils import read_user_config, save_user_config


def sync(workspace_id, directory):
    refresh_config()
