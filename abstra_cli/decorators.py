from abstra_cli.apis import get_auth_info, usage


def credentials_check(f):
    def wrapper(*args, **kwargs):
        api_token, workspace_id, author_id = get_auth_info()

        if not api_token:
            raise Exception("No API token configured")

        if not workspace_id:
            raise Exception("Bad token: no workspace found")

        usage(f, args, kwargs, author_id, workspace_id)
        return f(*args, **kwargs)

    return wrapper


def configuration_check(f):
    def wrapper(*args, **kwargs):
        api_token, workspace_id, author_id = get_auth_info()
        usage(f, args, kwargs, author_id, workspace_id)
        return f(*args, **kwargs)

    return wrapper
