import os


def create_abstra_dir():
    path = rebase_path("/.abstra")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def rebase_path(path="/"):
    return os.path.expanduser("~" + path)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text