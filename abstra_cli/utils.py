import os


def rebase_path(path="/"):
    return os.path.expanduser("~" + path)


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text
