from .utils_config import config_check, get_auth_config
from .apis import get_file_signed_url


@config_check
def get_file_url(filepath):
    api_token, workspace_id = get_auth_config()
    return get_file_signed_url(workspace_id, filepath, api_token)
