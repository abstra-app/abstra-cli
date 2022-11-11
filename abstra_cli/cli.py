import fire

import abstra_cli.cli_helpers as cli_helpers
import abstra_cli.utils_config as utils_config
import abstra_cli.messages as messages
from abstra_cli.resources import Forms, Files, Packages, Vars


class CLI(object):
    """
    A CLI to manage your Abstra Cloud Workspace environment.

    usage: abstra <command> <resource> [<argument> ...] [parameters]
    """

    @utils_config.configuration_check
    def configure(self, api_token=None):
        utils_config.save_credentials(api_token or cli_helpers.read_credentials())
        print("Done!")

    @utils_config.credentials_check
    def list(self, resource, **kwargs):
        list_func = {
            "vars": Vars.list,
            "files": Files.list,
            "packages": Packages.list,
            "forms": Forms.list,
        }.get(resource, messages.not_implemented)

        list_func()

    @utils_config.credentials_check
    def add(self, resource, *args, **kwargs):
        add_func = {
            "vars": Vars.add,
            "files": Files.add,
            "packages": Packages.add,
            "form": Forms.add,
        }.get(resource, messages.not_implemented)

        add_func(*args, **kwargs)

    @utils_config.credentials_check
    def update(self, resource, *args, **kwargs):
        update_func = {"form": Forms.update}.get(resource, messages.not_implemented)

        update_func(*args, **kwargs)

    @utils_config.credentials_check
    def remove(self, resource, *args, **kwargs):
        remove_func = {
            "vars": Vars.remove,
            "files": Files.remove,
            "packages": Packages.remove,
            "form": Forms.remove,
        }.get(resource, messages.not_implemented)

        remove_func(*args, **kwargs)

    @utils_config.credentials_check
    def play(self, resource, *args, **kwargs):
        play_func = {
            "form": Forms.play,
        }.get(resource, messages.not_implemented)

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
