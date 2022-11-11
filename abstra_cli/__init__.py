from abstra_cli.utils_config import credentials_check
from abstra_cli.apis import get_file_signed_url


@credentials_check
def get_file_url(filepath):
    return get_file_signed_url(filepath)
