import json
import requests
import urllib.request
import urllib.response

from .utils_config import get_auth_info, get_credentials

HACKERFORMS_API_URL = "https://hackerforms-api.abstra.cloud"
HACKERFORMS_HASURA_URL = "https://hackerforms-hasura.abstra.cloud/v1/graphql"


def hf_api_runner(method, path, data=None):
    api_token, workspace_id, _ = get_auth_info()
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


def delete_file(filepath):
    return hf_api_runner("DELETE", "file", {"filepath": filepath})


def hf_hasura_runner(query, variables={}):
    api_token = get_credentials()
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
    return jsond["errors"]


def list_workspace_packages():
    query = """
        query GetPackages {
            packages {
                name
                version
            }
        }
    """
    return hf_hasura_runner(query).get("packages", [])


def list_workspace_forms():
    query = """
        query GetForms {
            forms {
                id
                title
            }
        }
    """
    return hf_hasura_runner(query).get("forms", [])


def list_workspace_vars():
    query = """
        query GetVars {
            environment_variables {
                name
                value
            }
        }
    """
    return hf_hasura_runner(query).get("environment_variables", [])


def add_workspace_vars(raw_vars):
    _, workspace_id, _ = get_auth_info()
    vars = [
        {"name": v["name"], "value": v["value"], "workspace_id": workspace_id}
        for v in raw_vars
    ]
    query = """
        mutation InsertVars($vars: [environment_variables_insert_input!]!) {
            insert_environment_variables(
                objects: $vars
                on_conflict: {
                    constraint: environment_variables_name_workspace_id_key
                    update_columns: [value, name]
                }
            ) {
                returning {
                    name
                    value
                }
            }
        }
    """
    return (
        hf_hasura_runner(query, {"vars": vars})
        .get("insert_environment_variables", {})
        .get("returning", [])
    )


def add_workspace_packages(raw_packages):
    _, workspace_id, _ = get_auth_info()
    packages = [
        {"name": p["name"], "version": p["version"], "workspace_id": workspace_id}
        for p in raw_packages
    ]
    query = """
        mutation InsertPackages($packages: [packages_insert_input!]!) {
            insert_packages(
                objects: $packages
                on_conflict: {
                    constraint: packages_workspace_id_name_key  
                    update_columns: [version]
                }
            ) {
                returning {
                    name
                    version
                }
            }
        }
    """
    return (
        hf_hasura_runner(query, {"packages": packages})
        .get("insert_packages", {})
        .get("returning", [])
    )


def add_workspace_form(data):
    _, workspace_id = get_auth_info()
    form_data = {
        "title": data["name"],
        "workspace_id": workspace_id,
        "script": {
            "data": {
                "code": data["code"],
                "workspace_id": workspace_id,
                "name": data["name"],
            }
        },
    }

    data.pop("name")
    data.pop("code")
    form_data.update(data)

    query = """
        mutation InsertForm($form_data: [forms_insert_input!]!) {
            insert_forms(
                objects: $form_data
            ) {
                returning {
                    id
                    title
                    script {
                        id
                        code
                    }
                }
            }
        }
    """
    return (
        hf_hasura_runner(query, {"form_data": form_data})
        .get("insert_forms", {})
        .get("returning", {})
    )


def update_workspace_form(form_id, data):
    form_data = {}
    script_data = {}
    name = data.get("name", None)
    if name:
        data.pop("name")
        form_data["title"] = name
        script_data["name"] = name

    code = data.get("code", None)
    if code:
        data.pop("code")
        if "data" in script_data:
            script_data["code"] = code
        else:
            script_data = {}
            script_data["code"] = code

    for param, value in data.items():
        form_data[param] = value

    form_query = """
        mutation UpdateForm($id: uuid!, $form_data: forms_set_input, $script_data: scripts_set_input = {}) {
            update_forms_by_pk(pk_columns: {id: $id}, _set: $form_data) {
                id
                title
                script {
                    id
                    code
                }
            }
            $script_mutation
        }
    """

    if code or name:
        script = """
            update_scripts(where: {form: {id: {_eq: $id}}}, _set: $script_data) {
                returning {
                    name
                    code
                }
            }
        """
        form_query = form_query.replace("$script_mutation", script)
    else:
        form_query = form_query.replace("$script_mutation", "")

    return hf_hasura_runner(
        form_query, {"id": form_id, "form_data": form_data, "script_data": script_data}
    ).get("update_forms_by_pk", {})


def delete_workspace_packages(packages):
    query = """
        mutation DeletePackages($packages: [String!]) {
            delete_packages(where: {name: {_in: $packages}}) {
                returning {
                    name
                    version
                }
            }
        }
    """
    return (
        hf_hasura_runner(query, {"packages": packages})
        .get("delete_packages", {})
        .get("returning", [])
    )


def delete_workspace_vars(vars):
    query = """
        mutation DeleteVars($vars: [String!]) {
            delete_environment_variables(where: {name: {_in: $vars}}) {
                returning {
                    name
                    value
                }
            }
        }
    """
    return (
        hf_hasura_runner(query, {"vars": vars})
        .get("delete_environment_variables", {})
        .get("returning", [])
    )


def delete_workspace_form(form_id):
    query = """
    mutation DeleteForm($id: uuid!) {
        delete_forms_by_pk(id: $id) {
            id
        }
    }
    """

    return hf_hasura_runner(query, {"id": form_id})
