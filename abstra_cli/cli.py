import fire

from abstra_cli.cli_helpers import read_credentials
from abstra_cli.utils_config import credentials_check, save_credentials
from abstra_cli.messages import not_implemented

from abstra_cli.resources import Forms
from abstra_cli.resources import Files
from abstra_cli.resources import Packages
from abstra_cli.resources import Vars


class CLI(object):
    """
    A CLI to manage your Abstra Cloud Workspace environment.

    usage: abstra <command> <resource> [<argument> ...] [parameters]
    """

    def configure(self, api_token=None):
        credentials_check(self.configure, **api_token)
        save_credentials(api_token or read_credentials())
        print("Done!")

    def list(self, resource, **kwargs):
        """List all items of a selected resource in the configured workspace

        Args:
            resource: Available resources are \n
                - vars -> list all environment variables in workspace\n
                - files -> list all file names in workspace\n
                - packages -> list all packages in workspace\n
                - forms -> list all forms in workspace
        """
        credentials_check(self.list, resource, **kwargs)
        list_func = {
            "vars": Vars.list,
            "files": Files.list,
            "packages": Packages.list,
            "forms": Forms.list,
        }.get(resource, not_implemented)

        list_func()

    def add(self, resource, *args, **kwargs):
        credentials_check(self.add, *((resource,) + args), **kwargs)

        add_func = {
            "vars": Vars.add,
            "files": Files.add,
            "packages": Packages.add,
            "form": Forms.add,
        }.get(resource, not_implemented)

        add_func(*args, **kwargs)

    def update(self, resource, *args, **kwargs):
        credentials_check(self.update, *((resource,) + args), **kwargs)
        update_func = {"form": Forms.update}.get(resource, not_implemented)

        update_func(*args, **kwargs)

    def remove(self, resource, *args, **kwargs):
        credentials_check(self.remove, *((resource,) + args), **kwargs)
        remove_func = {
            "vars": Vars.remove,
            "files": Files.remove,
            "packages": Packages.remove,
            "form": Forms.remove,
        }.get(resource, not_implemented)

        remove_func(*args, **kwargs)

    def play(self, resource, *args, **kwargs):
        credentials_check(self.play, *((resource,) + args), **kwargs)
        play_func = {
            "form": Forms.play,
        }.get(resource, not_implemented)

        play_func(*args, **kwargs)

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


def _SeparateFlagArgs(args):
    try:
        index = args.index("--help")
        args = args[:index]
        return args, ["--help"]
    except ValueError:
        return args, []


def main():
    fire.core.parser.SeparateFlagArgs = _SeparateFlagArgs
    fire.Fire(CLI)
