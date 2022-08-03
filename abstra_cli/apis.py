import json
import requests
import urllib.request
import urllib.response

from .utils_config import get_auth_info

HACKERFORMS_API_URL = "https://hackerforms-api.abstra.cloud"


def hf_api_runner(method, path, data=None):
    api_token, workspace_id = get_auth_info()
    response = requests.request(
        method,
        f"{HACKERFORMS_API_URL}/workspaces/{workspace_id}/{path}",
        data=json.dumps(data) if data else None,
        headers={"content-type": "application/json", "API-Authorization": api_token},
    )
    return response.json()


def upload_file(filepath, file):
    response_json = hf_api_runner("POST", "put-url", {"filepath": filepath})
    req = urllib.request.Request(
        url=response_json["putURL"], method="PUT", data=file.read()
    )
    res = urllib.request.urlopen(req)
    return res.status < 400


def get_file_signed_url(filepath):
    response_json = hf_api_runner("POST", "get-url", {"filepath": filepath})
    return response_json.get("getURL")


def list_workspace_files():
    return hf_api_runner("GET", "files")


def list_workspace_packages():
    return hf_api_runner("GET", "packages")


def list_workspace_vars():
    return hf_api_runner("GET", "vars")
