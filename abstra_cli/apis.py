import json
import requests

from .utils import read_config


def upload_file(workspace_id, filepath, file):
    access_token = read_config()['access_token']
    response = requests.post(
        f"https://hackerforms-api.abstra.cloud/workspaces/{workspace_id}/put-url",
        data=json.dumps({'filepath': filepath}),
        headers={'content-type': 'application/json',
                 'Author-Authorization': f'Bearer {access_token}'}
    )
    response_json = response.json()
    r = requests.put(url=response_json["putURL"], data=file)
    return r.ok
