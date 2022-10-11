import os
from pathlib import Path
from abc import ABC, abstractmethod

from .cli_helpers import (
    print_files,
    print_packages,
    print_forms,
    print_vars,
    show_progress
)
from .file_utils import files_from_directory
from .utils import parse_env_var, parse_package, remove_from_dict
from .apis import (
    add_workspace_packages,
    add_workspace_vars,
    delete_file,
    delete_workspace_form,
    delete_workspace_packages,
    delete_workspace_vars,
    list_workspace_files,
    list_workspace_vars,
    list_workspace_packages,
    list_workspace_forms,
    upload_file,
)

from .messages import (
    form_created_message
)

from .services import (
    add_code
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

    @staticmethod
    @abstractmethod
    def remove(*args, **kwargs):
        pass


class Files(Resource):
    @staticmethod
    def list(*args, **kwargs):
        files = list_workspace_files()
        print_files(files)

    @staticmethod
    def add(*args, **kwargs):
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

    @staticmethod
    def remove(*args, **kwargs):
        # TODO: list first then delete
        bar = show_progress("Deleting files", len(args))
        for f in args:
            ok = delete_file(f)
            if not ok:
                print(f"Error deleting file {f}")
                return False
            else:
                bar.next()
        bar.finish()
        print(f"\nDeleted {len(args)} files successfully")


class Vars(Resource):
    @staticmethod
    def list(*args, **kwargs):
        vars = list_workspace_vars()
        print_vars(vars)

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
        print_vars(added_vars)
        print(f"\nAdded {len(added_vars)} enviroment variables")

    @staticmethod
    def remove(*args, **kwargs):
        deleted_vars = delete_workspace_vars(args)
        print_vars(deleted_vars)
        print(f"\nDeleted {len(deleted_vars)} vars")


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

class Forms(Resource):
    @staticmethod
    def list(*args, **kwargs):
        forms = list_workspace_forms()
        print_forms(forms)

    @staticmethod
    def add(*args, **kwargs):
        EMPTY_FORM = 'from hackerforms import *'

        name = kwargs.get("name") or kwargs.get("n")
        if not name:
            print("required parameter: --name [name]")
            exit()

        file = kwargs.get("file") or kwargs.get("f")
        if file:
            with open(file, "r") as f:
                code = f.read()
            remove_from_dict(['name', 'n', 'file', 'f'], kwargs)
            add_code(name, code, **kwargs)
            exit()

        code = kwargs.get("code") or kwargs.get("c")
        if code:
            remove_from_dict(['name', 'n', 'code', 'c'], kwargs)
            add_code(name, code, **kwargs)
            exit()

        add_code(name, EMPTY_FORM)



    @staticmethod
    def remove(*args, **kwargs):
        form_id = args[0]
        if not form_id:
            print("required parameter: [form_id]")
            exit()
        delete_workspace_form(args[0])
