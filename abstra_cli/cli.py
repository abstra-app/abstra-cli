import fire

from .utils_config import get_auth_config, config_check, save_config
from .apis import upload_file
from .file_utils import files_from_directory, remove_filepath_prefix

class CLI(object):

    def configure(self, api_token):
        save_config({'api_token': api_token})
        print("Done!")

    @config_check
    def upload(self, directory):
        api_token, workspace_id = get_auth_config()
        if workspace_id is None:
            return print("Bad API token")

        files = files_from_directory(directory)
        for path in files:
            filename = remove_filepath_prefix(path.as_posix(), directory)
            ok = upload_file(workspace_id, filename, path.open("rb"), api_token)
            if not ok:
                print(f"Error uploading file {filename}")
                return False
            else:
                print(f"Uploaded file {filename}")


def main():
    fire.Fire(CLI)
