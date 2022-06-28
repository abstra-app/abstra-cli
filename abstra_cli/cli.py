import fire
from pathlib import Path

from .utils_config import get_auth_config, config_check, save_config
from .apis import upload_file


class CLI(object):

    def configure(self, api_token):
        save_config({'api_token': api_token})
        print("Done!")

    @config_check
    def upload(self, directory):
        api_token, workspace_id = get_auth_config()
        if workspace_id is None:
            return print("Bad API token")

        files = [path for path in Path(directory).rglob('*') if path.is_file()]
        for path in files:
            filename = path.as_posix().removeprefix(directory)
            ok = upload_file(workspace_id, filename,
                             path.open("rb"), api_token)
            if not ok:
                print(f"Error uploading file {filename}")
                return False
            else:
                print(f"Uploaded file {filename}")


def main():
    fire.Fire(CLI)
