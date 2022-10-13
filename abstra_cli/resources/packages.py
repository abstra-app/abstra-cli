from abstra_cli.utils import parse_package
from abstra_cli.cli_helpers import print_packages
from abstra_cli.apis import (
    add_workspace_packages,
    list_workspace_packages,
    delete_workspace_packages,
)
from abstra_cli.resources.resources import Resource


class Packages(Resource):
    @staticmethod
    def list(*args, **kwargs):
        packages = list_workspace_packages()
        print_packages(packages)

    @staticmethod
    def add(*args, **kwargs):
        packages = list(args)
        file = (
            kwargs.get("f")
            or kwargs.get("file")
            or kwargs.get("r")
            or kwargs.get("requirement")
        )
        if file:
            with open(file, "r") as f:
                packages.extend([p for p in f.read().split("\n") if p])

        processed_packages = []
        processed_names = []
        for pkg in packages:
            name, version = parse_package(pkg)
            if not name:
                print(f"Invalid package: {pkg}")
                return False
            if name in processed_names:
                print(f"Duplicate package: {pkg}")
                return False
            processed_packages.append({"name": name, "version": version})

        added_packages = add_workspace_packages(processed_packages)
        print_packages(added_packages)
        print(f"\nAdded {len(added_packages)} packages")

    @staticmethod
    def remove(*args, **kwargs):
        deleted_packages = delete_workspace_packages(args)
        print_packages(deleted_packages)
        print(f"\nDeleted {len(deleted_packages)} packages")
