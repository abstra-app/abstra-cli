import os
import fnmatch
from pathlib import Path

from abstra_cli.utils import remove_prefix
from abstra_cli.utils_config import ABSTRA_FOLDER


def get_ignore_files(dir):
    IGNOREFILE = os.path.join(dir, ".abstraignore")
    abstra_path = os.path.join(dir, ABSTRA_FOLDER)
    ignored = [IGNOREFILE, abstra_path]
    if os.path.exists(IGNOREFILE):
        with open(IGNOREFILE, "r") as f:
            ignored.extend([os.path.join(dir, f) for f in f.read().split("\n") if f])
    return ignored


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
    ignored = [*get_ignore_files(directory), *get_ignore_files(os.getcwd())]
    paths = Path(directory).rglob("*")
    paths = [
        path for path in paths if path.is_file() and not should_ignore(ignored, path)
    ]
    return paths


def remove_filepath_prefix(filepath, prefix):
    return remove_prefix(normalize_path(filepath), normalize_path(prefix) + "/")
