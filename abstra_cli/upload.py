from pathlib import Path

from .utils_config import get_api_token
from .apis import upload_file, get_workspace_from_token


def upload(directory):
    api_token = get_api_token()
    workspace_id = get_workspace_from_token(api_token)
    if workspace_id is None:
        return print("Bad API token")

    files = [path for path in Path(directory).rglob('*') if path.is_file()]
    for path in files:
        filename = path.as_posix().removeprefix(directory)
        ok = upload_file(workspace_id, filename, path.open(), api_token)
        if not ok:
            print(f"Error uploading file {path.as_posix()}")
            return False
        else:
            print(f"Uploaded file {path.as_posix()}")
