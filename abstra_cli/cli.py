import fire

from .apis import upload_file
from .cli_helpers import read_api_token, show_progress
from .file_utils import files_from_directory, remove_filepath_prefix
from .utils_config import get_auth_config, token_check, save_api_token


class CLI(object):
    def configure(self, api_token=None):
        save_api_token(api_token or read_api_token())
        print("Done!")

    @token_check
    def upload(self, directory):
        api_token, workspace_id = get_auth_config()
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
