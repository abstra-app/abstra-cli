from abc import ABC, abstractmethod

from .apis import list_workspace_files, list_workspace_vars, list_workspace_packages


digits = lambda n: len(str(n))
format_digits = lambda n, d: " " * (d - digits(n)) + str(n)


class Resource(ABC):
    @staticmethod
    @abstractmethod
    def list(*args, **kwargs):
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


class Vars(Resource):
    @staticmethod
    def list(*args, **kwargs):
        vars = list_workspace_vars()
        vars.sort(key=lambda x: x["name"])
        for var in vars:
            print(f"{var['name']}={var['value']}")


class Packages(Resource):
    @staticmethod
    def list(*args, **kwargs):
        packages = list_workspace_packages()
        for pkg, version in packages.items():
            print(f"{pkg}{'=' + version if version else ''}")
