import fire

from .auth import refresh_config
from .utils import read_config
from .login import login
from .sync import sync


class CLI(object):

    def login(self):
        return login()

    def sync(self, workspace_id, directory):
        if not read_config():
            return print("Please login first")

        refresh_config()
        return sync(workspace_id, directory)


def main():
    fire.Fire(CLI)
