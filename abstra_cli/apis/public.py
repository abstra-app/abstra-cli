import os
import json
import requests
from functools import lru_cache


@lru_cache(maxsize=None)
def get_info_from_token(api_token):
    response = requests.get(
        f"https://auth.abstra.cloud/abstra-cloud",
        headers={"content-type": "application/json", "API-Authorization": api_token},
    )
    response_json = response.json()
    author_id = response_json.get("author_id")
    workspaces = response_json.get("workspaces", [{}])

    workspace_id = None
    if len(workspaces) != 0:
        workspace_id = workspaces[0].get("id")

    return workspace_id, author_id


def usage(f, args, kwargs, author_id, workspace_id):
    if os.getenv("DISABLE_USAGE_STATISTICS"):
        return

    try:
        requests.post(
            "https://usage-api.abstra.cloud/api/rest/cli-usage",
            data=json.dumps(
                {
                    "author_id": author_id,
                    "workspace_id": workspace_id,
                    "method": f.__name__,
                    "arguments": {"args": args[1:], "kwargs": list(kwargs.keys())},
                }
            ),
            headers={"content-type": "application/json"},
        )
    except Exception as e:
        pass
