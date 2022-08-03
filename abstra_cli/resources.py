import os
from pathlib import Path
from abc import ABC, abstractmethod

from .cli_helpers import show_progress
from .utils import format_digits, digits
from .file_utils import files_from_directory
from .apis import list_workspace_files, list_workspace_vars, list_workspace_packages, upload_file


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
            print(
                f"{format_digits(file['Size'], max_digits)} - {file['LastModified']}: {file['Key']}"
            )

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
        print("All files were uploaded!")


class Vars(Resource):
    @staticmethod
    def list(*args, **kwargs):
        vars = list_workspace_vars()
        vars.sort(key=lambda x: x["name"])
        for var in vars:
            print(f"{var['name']}={var['value']}")

    @staticmethod
    def add(*args, **kwargs):
        pass


class Packages(Resource):
    @staticmethod
    def list(*args, **kwargs):
        packages = list_workspace_packages()
        for pkg, version in packages.items():
            print(f"{pkg}{'=' + version if version else ''}")

    @staticmethod
    def add(*args, **kwargs):
        pass
