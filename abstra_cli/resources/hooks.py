import requests

from abstra_cli.resources.resources import Resource
import abstra_cli.cli_helpers as cli_helpers
import abstra_cli.messages as messages
import abstra_cli.utils as utils
import abstra_cli.apis as apis


NAME_PARAMETERS = ["name", "title"]
PATH_PARAMETERS = ["path"]
CODE_PARAMETERS = ["file", "f", "code", "c"]
NON_FLAG_PARAMETERS = NAME_PARAMETERS + PATH_PARAMETERS + CODE_PARAMETERS
FLAG_PARAMETERS = ["enabled"]
HOOK_PARAMETERS = FLAG_PARAMETERS + NON_FLAG_PARAMETERS


def check_valid_parameters(parameters: dict) -> None:
    for param in parameters.keys():
        if param not in HOOK_PARAMETERS:
            messages.invalid_parameter(param)
            exit()
    for param, value in parameters.items():
        if param in NON_FLAG_PARAMETERS and value in [True, False]:
            messages.invalid_non_flag_parameter_value(param)
            exit()


def evaluate_parameter_name(parameters: dict, use_default=True) -> dict:
    name = parameters.get("name") or parameters.get("n") or parameters.get("title")
    if not name and not use_default:
        return {}
    return {"name": name or "New Hook"}


def evaluate_parameter_path(parameters: dict) -> dict:
    path = parameters.get("path")
    if not path:
        return {}
    return {"path": path}


def evaluate_parameters_file_and_code(parameters: dict, use_default=True) -> dict:
    EMPTY_HOOk = "from abstra.hooks import get_request, send_json\nbody, query, headers = get_request()\nprint(body) # parsed json if content type is application/json, text otherwise\nprint(query, headers) # both dicts\nsend_json(data={'ok': True}, status_code=200, headers={'ABSTRA': 'CLOUD'})\n# send_response(body='plain text body')"
    file = parameters.get("file") or parameters.get("f")
    code = parameters.get("code") or parameters.get("c")

    if file and code:
        messages.code_and_file_not_allowed()
        exit()

    if file:
        with open(file, "r") as f:
            return {"code": f.read()}

    if code:
        return {"code": code}

    return {"code": EMPTY_HOOk} if use_default else {}


def evaluate_flag_parameters(parameters: dict) -> dict:
    evaluated_params = {}
    for param, value in parameters.items():
        if param in FLAG_PARAMETERS:
            if value == "true" or value == True:
                evaluated_params[param] = True
                continue
            if value == "false" or value == False:
                evaluated_params[param] = False
                continue

            messages.invalid_flag_parameter_value(param)
            exit()
    return evaluated_params


class Hooks(Resource):
    @staticmethod
    def list():
        hooks = apis.list_workspace_hooks()
        cli_helpers.print_hooks(hooks)

    @staticmethod
    def add(*args, **kwargs):
        upsert = kwargs.pop("upsert", False)
        path = kwargs.get("path")
        if upsert and not path:
            messages.upsert_without_identifier("path")
            exit()

        check_valid_parameters(kwargs)

        hook_data = {
            **evaluate_parameter_name(kwargs),
            **evaluate_parameter_path(kwargs),
            **evaluate_parameters_file_and_code(kwargs),
            **evaluate_flag_parameters(kwargs),
        }

        if hook_data:
            try:
                if upsert:
                    apis.upsert_workspace_hook(hook_data)
                    messages.upserted_message("Hook", path)
                else:
                    path = apis.add_workspace_hook(hook_data)["path"]
                    messages.created_message("Hook", path)
            except Exception as e:
                print(e)
                messages.create_failed(
                    "Hook",
                )

    @staticmethod
    def update(*args, **kwargs):

        if not len(args):
            messages.required_argument("path")
            exit()
        path = args[0]

        if not len(kwargs):
            messages.missing_parameters_to_update(path)
            exit()

        check_valid_parameters(kwargs)

        hook_data = {
            **evaluate_parameter_name(kwargs, use_default=False),
            **evaluate_parameter_path(kwargs),
            **evaluate_parameters_file_and_code(kwargs, use_default=False),
            **evaluate_flag_parameters(kwargs),
        }

        if hook_data:
            try:
                apis.update_workspace_hook(path, hook_data)
                messages.updated_message("Hook", path)
            except Exception as e:
                print(e)
                messages.update_failed("Hook", path)

    @staticmethod
    def remove(*args, **kwargs):
        if not len(args):
            messages.required_argument("path")
            exit()

        path = args[0]
        apis.delete_workspace_hook(path)
        messages.deleted_message("Hook", path)

    @staticmethod
    def play(*args, **kwargs):
        # TODO: add body and headers
        if not len(args):
            messages.required_argument("path")
            exit()

        method = kwargs.get("method") or kwargs.get("m") or "POST"
        path = args[0]

        subdomain_name = apis.get_subdomain()
        url = utils.get_prod_hook_url(subdomain_name, path)

        messages.hook_url(url, method)
        r = requests.request(method, url)
        print("Response:\n", r.text)
