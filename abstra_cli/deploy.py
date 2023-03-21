import json, sys
from abstra_cli.resources import Forms, Files, Packages, Vars, Hooks, Jobs, Dashes


ACCEPTED_KEYS = ["files", "workspace", "forms", "hooks", "jobs", "packages", "vars"]


def get_abstra_json_path(parameters: dict) -> str:
    return parameters.get("file") or parameters.get("f") or "abstra.json"


def evaluate_parameters_file(parameters: dict) -> dict:
    file = get_abstra_json_path(parameters)

    data = None
    try:
        with open(file) as f:
            data = json.loads(f.read())
            if not isinstance(data, dict):
                print("Bad data")
                sys.exit(1)
    except:
        print("Deploy file not found or not correct format")
        sys.exit(1)

    for key in data.keys():
        if key not in ACCEPTED_KEYS:
            print(f"Extra data in deploy file {file} not accepted")
            sys.exit(1)

    return data


def deploy(**kwargs):
    deploy_data = evaluate_parameters_file(kwargs)

    dashes = Dashes.get_deploy_data(get_abstra_json_path(kwargs))
    if len(dashes):
        for dash_props in dashes:
            Dashes.add(upsert=True, **dash_props)

        remote_dashes_files = Files.list_dashes_files(".")
        local_dashes_files = [
            d["code"].replace(".py", ".abstradash.json") for d in dashes
        ]
        deleted_dashes_files = [
            f for f in remote_dashes_files if f not in local_dashes_files
        ]

        for deleted_dash_file in deleted_dashes_files:
            deleted_dash_path = deleted_dash_file.replace(
                ".abstradash.json", ""
            ).replace(f"./", "")
            Dashes.remove(deleted_dash_path)
            Files.remove(
                deleted_dash_file, deleted_dash_file.replace(".abstradash.json", ".py")
            )

    forms = deploy_data.pop("forms", None)
    if forms:
        for form in forms:
            Forms.add(upsert=True, **form)

    hooks = deploy_data.pop("hooks", None)
    if hooks:
        for hook in hooks:
            Hooks.add(upsert=True, **hook)

    jobs = deploy_data.pop("jobs", None)
    if jobs:
        for job in jobs:
            Jobs.add(upsert=True, **job)

    files = deploy_data.pop("files", ["."])  # review security implications
    if files:
        if isinstance(files, dict):
            Files.add(**files)
        elif isinstance(files, list):
            Files.add(*files)

    packages = deploy_data.pop("packages", {"requirement": "requirements.txt"})
    if packages:
        if isinstance(packages, dict):
            Packages.add(**packages)
        elif isinstance(packages, list):
            Packages.add(*packages)

    vars = deploy_data.pop("vars", None)
    if vars:
        if isinstance(vars, dict):
            Vars.add(**vars)
        elif isinstance(vars, list):
            Vars.add(*vars)
