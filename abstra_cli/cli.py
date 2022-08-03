import fire

from .apis import upload_file
from .cli_helpers import read_credentials, show_progress
from .file_utils import files_from_directory, remove_filepath_prefix
from .utils_config import credentials_check, save_credentials
from .resources import Files, Vars, Packages


def not_implemented(*args, **kwargs):
    print("Not implemented yet")


class CLI(object):
    def configure(self, api_token=None):
        save_credentials(api_token or read_credentials())
        print("Done!")

    @credentials_check
    def upload(self, directory="."):
        files = files_from_directory(directory)
        bar = show_progress("Uploading files", len(files))

        for path in files:
            filename = remove_filepath_prefix(path.as_posix(), directory)
            ok = upload_file(filename, path.open("rb"))
            if not ok:
                print(f"Error uploading file {filename}")
                return False
            else:
                bar.next()
        bar.finish()
        print("All files were uploaded!")

    @credentials_check
    def list(self, resource, *args, **kwargs):
        list_func = {
            "files": Files.list,
            "vars": Vars.list,
            "packages": Packages.list,
        }.get(resource, not_implemented)

        list_func(*args, **kwargs)


def main():
    fire.Fire(CLI)
