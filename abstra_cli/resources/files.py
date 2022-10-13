import os
from pathlib import Path

from abstra_cli.resources.resources import Resource
from abstra_cli.apis import (
    delete_file,
    list_workspace_files,
    upload_file,
)

from abstra_cli.cli_helpers import print_files, show_progress
from abstra_cli.file_utils import files_from_directory


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
