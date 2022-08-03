import fire

from .cli_helpers import read_credentials
from .utils_config import credentials_check, save_credentials
from .resources import Files, Vars, Packages


def not_implemented(*args, **kwargs):
    print("Not implemented yet")


class CLI(object):
    def configure(self, api_token=None):
        save_credentials(api_token or read_credentials())
        print("Done!")

    @credentials_check
    def list(self, resource, *args, **kwargs):
        list_func = {
            "files": Files.list,
            "vars": Vars.list,
            "packages": Packages.list,
        }.get(resource, not_implemented)

        list_func(*args, **kwargs)

    @credentials_check
    def add(self, resource, *args, **kwargs):
        add_func = {
            "files": Files.add,
            "vars": Vars.add,
            "packages": Packages.add,
        }.get(resource, not_implemented)

        add_func(*args, **kwargs)

    # Aliases
    @credentials_check
    def upload(self, *args):
        if not len(args):
            args = ["."]
        self.add("files", *args)

    @credentials_check
    def ls(self):
        self.list("files")

    @credentials_check
    def install(self, *args, **kwargs):
        self.add("packages", *args, **kwargs)


def main():
    fire.Fire(CLI)
