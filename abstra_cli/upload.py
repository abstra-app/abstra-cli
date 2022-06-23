from pathlib import Path
import os
from .utils_config import get_api_token
from .apis import upload_file, get_workspace_from_token


def should_ignore(ignored_paths, _path):
    path = str(_path)
    for ignored_path in ignored_paths:
        if ignored_path == path:
            return True
        if path.startswith(ignored_path + "/"):
            return True
    return False

def normalize_path(path):
    if path.endswith("/"):
        return path[:-1]
    return path

def files_from_directory(directory):
    ignorefile = directory + "/.abstraignore"
    if os.path.exists(ignorefile):
        with open(ignorefile, "r") as f:
            ignored = [directory + "/" + normalize_path(path) for path in f.read().split("\n")]
    else:
        ignored = []

    paths = Path(directory).rglob('*')
    paths =  [
        path
        for path in paths
        if path.is_file() and not should_ignore(ignored, path) and (str(path) != ignorefile)
    ]
    return paths

def upload(directory):
    api_token = get_api_token()
    workspace_id = get_workspace_from_token(api_token)
    if workspace_id is None:
        return print("Bad API token")

    files = files_from_directory(directory)
    for path in files:
        filename = path.as_posix().removeprefix(directory)
        ok = upload_file(workspace_id, filename, path.open("rb"), api_token)
        if not ok:
            print(f"Error uploading file {filename}")
            return False
        else:
            print(f"Uploaded file {filename}")
