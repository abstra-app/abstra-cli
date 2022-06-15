import fire

from .login import login
from .sync import sync


class CLI(object):

    def login(self):
        return login()

    def sync(self, workspace_id, directory):
        return sync(workspace_id, directory)


def main():
    fire.Fire(CLI)
