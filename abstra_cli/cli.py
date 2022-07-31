import fire
from progress.bar import FillingSquaresBar

from .utils_config import get_auth_config, config_check, save_config
from .apis import upload_file
from .file_utils import files_from_directory, remove_filepath_prefix
from .cli_helpers import request_api_token_from_user
class CLI(object):
    def configure(self, api_token=None):
        if not api_token:
            request_api_token_from_user()
            return
        save_config({'api_token': api_token})
        print("API Token saved")

    @config_check
    def upload(self, directory: str):
        api_token, workspace_id = get_auth_config()
        if workspace_id is None:
            return print("abstra: error: Bad API token")

        files = files_from_directory(directory)
        bar = FillingSquaresBar('Uploading files', suffix='%(percent)d%%', max=len(files))

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
