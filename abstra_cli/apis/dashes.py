import abstra_cli.apis.main as api_main
import abstra_cli.utils as utils


def list_workspace_dashes():
    query = """
        query GetDashes {
            dashes {
                path
                title
                script {
                    enabled
                }
            }
        }
    """
    return api_main.hf_hasura_runner(query).get("dashes", [])


def add_workspace_dash(data):
    _, workspace_id, _ = api_main.get_auth_info()
    dash_data = {
        "title": data["name"],
        "workspace_id": workspace_id,
        "draft_layout": None,
        "theme": data.get("theme", None),
        "script": {
            "data": {
                "workspace_id": workspace_id,
                "enabled": data.get("enabled", True),
                "file_path": data["code_file_path"],
                "name": data["name"],
            }
        },
    }

    query = """
        mutation InsertDash($dash_data: [dashes_insert_input!]!) {
            insert_dashes(
                objects: $dash_data
            ) {
                returning {
                    path
                    title
                }
            }
        }
    """

    return (
        api_main.hf_hasura_runner(query, {"dash_data": dash_data})
        .get("insert_dashes", {})
        .get("returning", {})[0]
    )


def update_workspace_dash(path, data):
    dash_data = {
        "title": data["name"],
        "draft_layout": None,
        "theme": data.get("theme", None)
    }
    script_data = {
        "enabled": data.get("enabled", True),
        "file_path": data["code_file_path"],
        "code": None,
        "name": data["name"],
    }

    request_data = {"path": path, "dash_data": dash_data, "script_data": script_data}
    update_query = """
        mutation UpdateDash($path: String!, $dash_data: dashes_set_input, $script_data: scripts_set_input = {}) {
            update_dashes(where: {path: {_eq: $path}}, _set: $dash_data) {
                returning {
                    id
                    path
                    title
                }
            }
            update_scripts(where: {dash: {path: {_eq: $path}}}, _set: $script_data) {
                returning {
                    name
                }
            }
        }
    """
    return (
        api_main.hf_hasura_runner(update_query, request_data)
            .get("update_dashes", {})
            .get("returning", {})[0]
    )


def upsert_workspace_dash(data):
    path = data["path"]

    query = """
        query FindDash($path: String!) {
            dashes(where: {path: {_eq: $path}}) {
                path
            }
        }
    """

    dashes = api_main.hf_hasura_runner(query, {"path": path}).get("dashes")
    if len(dashes):
        return update_workspace_dash(path, data)
    else:
        return add_workspace_dash(data)


def delete_workspace_dash(path):
    query = """
        mutation DeleteDash($path: String!) {
            delete_dashes(where: {path: {_eq: $path}}) {
                returning {
                    id
                    path
                    title
                }
            }
        }
    """

    return api_main.hf_hasura_runner(query, {"path": path})
