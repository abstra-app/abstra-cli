from abstra_cli.resources.resources import Resource
import abstra_cli.cli_helpers as cli_helpers
import abstra_cli.messages as messages
import abstra_cli.utils as utils
import abstra_cli.apis as apis


class Vars(Resource):
    @staticmethod
    def list():
        vars = apis.list_workspace_vars()
        cli_helpers.print_vars(vars)

    @staticmethod
    def add(*args, **kwargs):
        vars = list(args)
        file = kwargs.get("f") or kwargs.get("file")
        if file:
            with open(file, "r") as f:
                vars.extend([v for v in f.read().split("\n") if v])

        processed_vars = []
        processed_names = []
        for var in vars:
            name, value = utils.parse_env_var(var)
            if not name or not value:
                messages.invalid_variable(var)
                return False
            if name in processed_names:
                messages.duplicate_variable(var)
                return False
            processed_vars.append({"name": name, "value": value})

        added_vars = apis.add_workspace_vars(processed_vars)
        cli_helpers.print_vars(added_vars)
        print(f"\nAdded {len(added_vars)} enviroment variables")

    @staticmethod
    def remove(*args, **kwargs):
        deleted_vars = apis.delete_workspace_vars(args)
        cli_helpers.print_vars(deleted_vars)
        print(f"\nDeleted {len(deleted_vars)} vars")
