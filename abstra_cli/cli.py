import fire

from .cli_helpers import read_credentials
from .utils_config import credentials_check, save_credentials
from .resources import Files, Vars, Packages, Forms


def not_implemented(*args, **kwargs):
    print("Invalid command")


class CLI(object):
    def configure(self, api_token=None):
        save_credentials(api_token or read_credentials())
        print("Done!")

    @credentials_check
    def list(self, resource, *args, **kwargs):
        list_func = {
            "vars": Vars.list,
            "files": Files.list,
            "packages": Packages.list,
            "forms": Forms.list,
        }.get(resource, not_implemented)

        list_func(*args, **kwargs)

    @credentials_check
    def add(self, resource, *args, **kwargs):
        add_func = {
            "vars": Vars.add,
            "files": Files.add,
            "packages": Packages.add,
            "form": Forms.add
        }.get(resource, not_implemented)

        add_func(*args, **kwargs)

    @credentials_check
    def remove(self, resource, *args, **kwargs):
        add_func = {
            "vars": Vars.remove,
            "files": Files.remove,
            "packages": Packages.remove,
        }.get(resource, not_implemented)

        add_func(*args, **kwargs)

    # Aliases
    @credentials_check
    def upload(self, *args, **kwargs):
        if not len(args):
            args = ["."]
        self.add("files", *args, **kwargs)

    @credentials_check
    def ls(self, *args, **kwargs):
        self.list("files", *args, **kwargs)

    @credentials_check
    def rm(self, *args, **kwargs):
        self.remove("files", *args, **kwargs)

    @credentials_check
    def install(self, *args, **kwargs):
        self.add("packages", *args, **kwargs)


def main():
    fire.Fire(CLI)
