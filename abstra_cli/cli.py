import fire

from abstra_cli.deploy import deploy
import abstra_cli.messages as messages
import abstra_cli.decorators as decorators
import abstra_cli.credentials as credentials
from abstra_cli.resources import Forms, Files, Packages, Vars, Hooks, Jobs, Dashes


class CLI(object):
    """
    A CLI to manage your Abstra Cloud Workspace environment.

    usage: abstra <command> <resource> [<argument> ...] [parameters]
    """

    @decorators.configuration_check
    def configure(self, api_token=None):
        credentials.save_credentials(api_token or messages.read_credentials())
        print("Done!")

    @decorators.credentials_check
    def list(self, resource, **kwargs):
        list_func = {
            "vars": Vars.list,
            "jobs": Jobs.list,
            "files": Files.list,
            "forms": Forms.list,
            "hooks": Hooks.list,
            "dashes": Dashes.list,
            "packages": Packages.list,
        }.get(resource, messages.not_implemented)

        list_func()

    @decorators.credentials_check
    def add(self, resource, *args, **kwargs):
        add_func = {
            "vars": Vars.add,
            "dash": Dashes.add,
            "dashes": Dashes.add,
            "form": Forms.add,
            "forms": Forms.add,
            "hook": Hooks.add,
            "hooks": Hooks.add,
            "job": Jobs.add,
            "jobs": Jobs.add,
            "files": Files.add,
            "packages": Packages.add,
        }.get(resource, messages.not_implemented)

        add_func(*args, **kwargs)

    @decorators.credentials_check
    def update(self, resource, *args, **kwargs):
        update_func = {
            "dash": Dashes.update,
            "dashes": Dashes.update,
            "form": Forms.update,
            "forms": Forms.update,
            "hook": Hooks.update,
            "hooks": Hooks.update,
            "job": Jobs.update,
            "jobs": Jobs.update,
        }.get(resource, messages.not_implemented)

        update_func(*args, **kwargs)

    @decorators.credentials_check
    def remove(self, resource, *args, **kwargs):
        remove_func = {
            "vars": Vars.remove,
            "dash": Dashes.remove,
            "dashes": Dashes.remove,
            "form": Forms.remove,
            "forms": Forms.remove,
            "hook": Hooks.remove,
            "hooks": Hooks.remove,
            "job": Jobs.remove,
            "jobs": Jobs.remove,
            "files": Files.remove,
            "packages": Packages.remove,
        }.get(resource, messages.not_implemented)

        remove_func(*args, **kwargs)

    @decorators.credentials_check
    def play(self, resource, *args, **kwargs):
        play_func = {
            "dash": Dashes.play,
            "form": Forms.play,
            "hook": Hooks.play,
            "forms": Forms.play,
            "hooks": Hooks.play,
        }.get(resource, messages.not_implemented)

        play_func(*args, **kwargs)

    @decorators.credentials_check
    def deploy(self, **kwargs):
        deploy(**kwargs)

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
