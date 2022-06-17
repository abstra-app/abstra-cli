import fire

from .utils_config import config_check
from .configure import configure
from .upload import upload


class CLI(object):

    def configure(self, api_token):
        return configure(api_token)

    @config_check
    def upload(self, directory):
        return upload(directory)


def main():
    fire.Fire(CLI)
