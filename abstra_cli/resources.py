import os
from pathlib import Path
from abc import ABC, abstractmethod

from .cli_helpers import print_file, print_package, print_var, show_progress
from .file_utils import files_from_directory
from .utils import digits, parse_env_var, parse_package
from .apis import (
    add_workspace_packages,
    add_workspace_vars,
    list_workspace_files,
    list_workspace_vars,
    list_workspace_packages,
    upload_file,
)


class Resource(ABC):
    @staticmethod
    @abstractmethod
    def list(*args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def add(*args, **kwargs):
        pass


class Files(Resource):
    @staticmethod
    def list(*args, **kwargs):
        files = list_workspace_files()
        files.sort(key=lambda x: x["Key"])
        max_digits = digits(max([f["Size"] for f in files]))
        for file in files:
            print_file(file, max_digits)

    @staticmethod
    def add(*args, **kwargs):
        if len(args) == 0:
            return print("Nothing to upload")

        files: list[Path] = []
        for path in args:
            if os.path.isfile(path):
                files.append(Path(path))
            elif os.path.isdir(path):
                files.extend(files_from_directory(path))

        bar = show_progress("Uploading files", len(files))
        for path in files:
            filename = path.as_posix()
            ok = upload_file(filename, path.open("rb"))
            if not ok:
                print(f"Error uploading file {filename}")
                return False
            else:
                bar.next()
        bar.finish()
        print(f"\nUploaded {len(files)} files successfully")


class Vars(Resource):
    @staticmethod
    def list(*args, **kwargs):
        vars = list_workspace_vars()
        vars.sort(key=lambda x: x["name"])
        for var in vars:
            print_var(var)

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
            name, value = parse_env_var(var)
            if not name or not value:
                print(f"Invalid variable: {var}")
                return False
            if name in processed_names:
                print(f"Duplicate variable: {var}")
                return False
            processed_vars.append({"name": name, "value": value})

        added_vars = add_workspace_vars(processed_vars)
        added_vars.sort(key=lambda x: x["name"])
        for var in added_vars:
            print_var(var)
        print(f"\nAdded {len(added_vars)} enviroment variables")


class Packages(Resource):
    @staticmethod
    def list(*args, **kwargs):
        packages = list_workspace_packages()
        packages.sort(key=lambda x: x["name"])
        for pkg in packages:
            print_package(pkg)

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
        added_packages.sort(key=lambda x: x["name"])
        for pkg in added_packages:
            print_package(pkg)
        print(f"\nAdded {len(added_packages)} packages")
