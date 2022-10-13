
import fire

from abstra_cli.cli_helpers import read_credentials
from abstra_cli.utils_config import credentials_check, save_credentials
from abstra_cli.messages import not_implemented

from abstra_cli.resources import Forms
from abstra_cli.resources import Files
from abstra_cli.resources import Packages
from abstra_cli.resources import Vars


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
    def update(self, resource, *args, **kwargs):
        update_func = {
            "form": Forms.update
        }.get(resource, not_implemented)

        update_func(*args, **kwargs)


    @credentials_check
    def remove(self, resource, *args, **kwargs):
        remove_func = {
            "vars": Vars.remove,
            "files": Files.remove,
            "packages": Packages.remove,
            "form": Forms.remove
        }.get(resource, not_implemented)

        remove_func(*args, **kwargs)

    # Aliases
    def upload(self, *args, **kwargs):
        if not len(args):
            args = ["."]
        self.add("files", *args, **kwargs)

    def ls(self, *args, **kwargs):
        self.list("files", *args, **kwargs)

    def rm(self, *args, **kwargs):
        self.remove("files", *args, **kwargs)

    def install(self, *args, **kwargs):
        self.add("packages", *args, **kwargs)


def main():
    fire.Fire(CLI)
