from .utils_config import credentials_check, get_auth_info
from .apis import get_file_signed_url


@credentials_check
def get_file_url(filepath):
    api_token, workspace_id = get_auth_info()
    return get_file_signed_url(workspace_id, filepath, api_token)
