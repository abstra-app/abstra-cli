import json
import requests
import urllib.request
import urllib.response
from functools import cache

from .utils_config import get_auth_info


def upload_file(filepath, file):
    api_token, workspace_id = get_auth_info()
    response = requests.post(
        f"https://hackerforms-api.abstra.cloud/workspaces/{workspace_id}/put-url",
        data=json.dumps({"filepath": filepath}),
        headers={"content-type": "application/json", "API-Authorization": api_token},
    )
    response_json = response.json()
    req = urllib.request.Request(
        url=response_json["putURL"], method="PUT", data=file.read()
    )
    res = urllib.request.urlopen(req)
    return res.status < 400


def get_file_signed_url(filepath):
    api_token, workspace_id = get_auth_info()
    response = requests.post(
        f"https://hackerforms-api.abstra.cloud/workspaces/{workspace_id}/get-url",
        data=json.dumps({"filepath": filepath}),
        headers={"content-type": "application/json", "API-Authorization": api_token},
    )
    response_json = response.json()
    return response_json.get("getURL")


@cache
def get_workspace_from_token(api_token):
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
