from abstra_cli.apis import (
    add_workspace_vars,
    list_workspace_vars,
    delete_workspace_vars,
)
from abstra_cli.cli_helpers import print_vars
from abstra_cli.resources.resources import Resource
from abstra_cli.utils import parse_env_var

from abstra_cli.messages import (
    invalid_variable,
    duplicate_variable,
)


class Vars(Resource):
    @staticmethod
    def list():
        vars = list_workspace_vars()
        print_vars(vars)

    @staticmethod
    def add(*args, **kwargs):
        print(args, kwargs)
        vars = list(args)
        file = kwargs.get("f") or kwargs.get("file")
        if file:
            with open(file, "r") as f:
                vars.extend([v for v in f.read().split("\n") if v])

        processed_vars = []
        processed_names = []
        for var in vars:
            name, value = parse_env_var(var)
            if not name or not value:
                invalid_variable(var)
                return False
            if name in processed_names:
                duplicate_variable(var)
                return False
            processed_vars.append({"name": name, "value": value})

        added_vars = add_workspace_vars(processed_vars)
        print_vars(added_vars)
        print(f"\nAdded {len(added_vars)} enviroment variables")

    @staticmethod
    def remove(*args, **kwargs):
        deleted_vars = delete_workspace_vars(args)
        print_vars(deleted_vars)
        print(f"\nDeleted {len(deleted_vars)} vars")
