from .utils_config import credentials_check
from .apis import get_file_signed_url


@credentials_check
def get_file_url(filepath):
    return get_file_signed_url(filepath)
