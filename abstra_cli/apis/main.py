import json
import requests
import urllib.request
import urllib.response
import abstra_cli.utils_config as utils_config


HACKERFORMS_API_URL = "https://hackerforms-api.abstra.cloud"
HACKERFORMS_HASURA_URL = "https://hackerforms-hasura.abstra.cloud/v1/graphql"
ABSTRA_ASSETS_UPLOAD_URL = "https://upload.abstra.cloud"


def asset_upload(filepath, file):
    response = requests.request(
        "POST",
        f"{ABSTRA_ASSETS_UPLOAD_URL}/asset/",
        headers={
            "cache-control": "no-cache",
            "Pragma": "no-cache",
            "content-type": "application/json",
        },
        data=json.dumps({"filepath": filepath}),
    )

    response_json = response.json()
    try:

        req = urllib.request.Request(
            url=response_json["putURL"], method="PUT", data=file
        )
        res = urllib.request.urlopen(req)
        if res.status < 400:
            return response_json["getURL"]
    except Exception as e:
        print(e)

    raise Exception("Some error ocurred in asset upload")


def hf_api_runner(method, path, data=None):
    api_token, workspace_id, _ = utils_config.get_auth_info()
    response = requests.request(
        method,
        f"{HACKERFORMS_API_URL}/workspaces/{workspace_id}/{path}",
        data=json.dumps(data) if data else None,
        headers={"content-type": "application/json", "API-Authorization": api_token},
    )
    return response.json()


def hf_hasura_runner(query, variables={}):
    api_token = utils_config.get_credentials()
    response = requests.post(
        HACKERFORMS_HASURA_URL,
        data=json.dumps({"query": query, "variables": variables}),
        headers={"content-type": "application/json", "API-Authorization": api_token},
    )
    if response.status_code >= 300:
        raise Exception(f"Request error: {response.text}")
    jsond = response.json()

    if "data" in jsond:
        return jsond["data"]

    raise Exception(jsond["errors"])


def get_subdomain():
    query = """
        query Subdomains {
            subdomains {
                name
            }
        }
    """

    subdomains = hf_hasura_runner(query, {}).get("subdomains", [])
    if not len(subdomains):
        print("Could not find subdomain.")
        exit()

    return subdomains[0]["name"]
