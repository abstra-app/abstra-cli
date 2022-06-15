import fire

from .login import login


class CLI(object):

    def login(self):
        return login()


def main():
    fire.Fire(CLI)
