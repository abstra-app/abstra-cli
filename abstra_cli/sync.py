from pathlib import Path

from .apis import upload_file


def sync(workspace_id, directory):
    files = [path for path in Path(directory).rglob('*') if path.is_file()]
    for path in files:
        ok = upload_file(workspace_id, path.as_posix(), path.open())
        if not ok:
            print(f"Error uploading file {path.as_posix()}")
            return False
        else:
            print(f"Uploaded file {path.as_posix()}")
