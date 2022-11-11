import os
from pathlib import Path

from abstra_cli.resources.resources import Resource
import abstra_cli.cli_helpers as cli_helpers
import abstra_cli.file_utils as file_utils
import abstra_cli.apis as apis


class Files(Resource):
    @staticmethod
    def list():
        files = apis.list_workspace_files()
        cli_helpers.print_files(files)

    @staticmethod
    def add(*args, **kwargs):
        files: list[Path] = []
        for path in args:
            if os.path.isfile(path):
                files.append(Path(path))
            elif os.path.isdir(path):
                files.extend(file_utils.files_from_directory(path))

        bar = cli_helpers.show_progress("Uploading files", len(files))
        for path in files:
            filename = path.as_posix()
            ok = apis.upload_file(filename, path.open("rb"))
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
        bar = cli_helpers.show_progress("Deleting files", len(args))
        for f in args:
            ok = apis.delete_file(f)
            if not ok:
                print(f"Error deleting file {f}")
                return False
            else:
                bar.next()
        bar.finish()
        print(f"\nDeleted {len(args)} files successfully")
