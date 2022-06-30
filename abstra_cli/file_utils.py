from pathlib import Path
import os
import fnmatch


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

def remove_filepath_prefix(filepath, prefix):
    return normalize_path(filepath).removeprefix(normalize_path(prefix) + "/")