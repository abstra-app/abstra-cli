from abstra_cli.apis import get_auth_info, usage


def credentials_check(fname, *args, **kwargs):
    api_token, workspace_id, author_id = get_auth_info()

    if not api_token:
        raise Exception("No API token configured")

    if not workspace_id:
        raise Exception("Bad token: no workspace found")

    usage(fname, args, kwargs, author_id, workspace_id)


def configuration_check(fname, *args, **kwargs):
    api_token, workspace_id, author_id = get_auth_info()
    usage(fname, args, kwargs, author_id, workspace_id)
