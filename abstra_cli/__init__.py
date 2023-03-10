from abstra_cli.checkers import credentials_check
from abstra_cli.apis import get_file_signed_url


def get_file_url(filepath):
    credentials_check("get_file_url", filepath)
    return get_file_signed_url(filepath)
