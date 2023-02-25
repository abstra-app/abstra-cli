import json
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
                raise Exception("Bad data")
    except:
        raise Exception("Deploy file not found or not correct format")

    for key in data.keys():
        if key not in ACCEPTED_KEYS:
            raise Exception(f"Extra data in deploy file {file} not accepted")

    return data


def deploy(**kwargs):
    deploy_data = evaluate_parameters_file(kwargs)

    for dash_props in Dashes.list_dash_props(get_abstra_json_path(kwargs)):
        Dashes.add(upsert=True, **dash_props)

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

    files = deploy_data.pop("files", None)
    if files:
        if isinstance(files, dict):
            Files.add(**files)
        elif isinstance(files, list):
            Files.add(*files)

    packages = deploy_data.pop("packages", None)
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
