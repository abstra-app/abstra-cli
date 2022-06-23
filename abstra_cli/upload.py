from pathlib import Path
import os
import fnmatch
from .utils_config import get_api_token
from .apis import upload_file, get_workspace_from_token


def should_ignore(ignored_paths, _path):
    path = str(_path)
    for _ignored_path in ignored_paths:
        ignored_path = normalize_path(_ignored_path)
        if fnmatch.fnmatch(path, ignored_path):
            return True
        if fnmatch.fnmatch(path, ignored_path + "/*"):
            return True
    return False

def normalize_path(path):
    path = str(path)
    if path.endswith("/"):
        path = path[:-1]
    if path.startswith("./"):
        path = path[2:]
    return path

def files_from_directory(directory):
    ignorefile = os.path.join(directory, ".abstraignore")
    if os.path.exists(ignorefile):
        with open(ignorefile, "r") as f:
            ignored = [os.path.join(directory, path) for path in f.read().split("\n")]
    else:
        ignored = []
    ignored.append(ignorefile)

    paths = Path(directory).rglob('*')
    paths =  [
        path
        for path in paths
        if path.is_file() and not should_ignore(ignored, path)
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
