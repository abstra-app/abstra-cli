import fire

from .apis import upload_file
from .cli_helpers import read_credentials, show_progress
from .file_utils import files_from_directory, remove_filepath_prefix
from .utils_config import get_auth_info, credentials_check, save_credentials


class CLI(object):
    def configure(self, api_token=None):
        save_credentials(api_token or read_credentials())
        print("Done!")

    @credentials_check
    def upload(self, directory="."):
        api_token, workspace_id = get_auth_info()
        if workspace_id is None:
            return print("Error: Bad API token")

        files = files_from_directory(directory)
        bar = show_progress("Uploading files", len(files))

        for path in files:
            filename = remove_filepath_prefix(path.as_posix(), directory)
            ok = upload_file(workspace_id, filename, path.open("rb"), api_token)
            if not ok:
                print(f"Error uploading file {filename}")
                return False
            else:
                bar.next()
        bar.finish()
        print("All files were uploaded!")


def main():
    fire.Fire(CLI)
