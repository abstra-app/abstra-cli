import sys
from abstra_cli.apis import get_auth_info, usage


def credentials_check(fname, *args, **kwargs):
    api_token, workspace_id, author_id = get_auth_info()

    if not api_token:
        print("No API token configured")
        sys.exit(1)

    if not workspace_id:
        print("Bad token: no workspace found")
        sys.exit(1)

    usage(fname, args, kwargs, author_id, workspace_id)


def configuration_check(fname, *args, **kwargs):
    api_token, workspace_id, author_id = get_auth_info()
    usage(fname, args, kwargs, author_id, workspace_id)


def is_logged():
    api_token, workspace_id, author_id = get_auth_info()
    return api_token and workspace_id
