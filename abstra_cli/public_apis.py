import json
import requests
from functools import cache


@cache
def get_workspace_from_token(api_token):
    print("Getting workspace from token")
    response = requests.post(
        f"https://auth.abstra.cloud/abstra-cloud",
        data=json.dumps({"headers": {"API-Authorization": api_token}}),
        headers={"content-type": "application/json"},
    )
    response_json = response.json()
    workspaces = response_json.get("workspaces", [{}])
    if len(workspaces) == 0:
        return None
    return workspaces[0].get("id")
