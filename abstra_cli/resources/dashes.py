import webbrowser


from abstra_cli.resources.resources import Resource
import abstra_cli.messages as messages
import abstra_cli.utils as utils
import abstra_cli.apis as apis
import os
import json
from glob import glob


NAME_PARAMETERS = ["name", "title"]
PATH_PARAMETERS = ["path"]
CODE_PARAMETERS = ["code", "c"]
BACKGROUND_PARAMETERS = ["background"]
OTHER_PARAMETERS = [
    "main_color",
    "font_family",
    "logo_url",
    "log_messages",
    "brand_name",
]
LAYOUT_PARAMETERS = ["layout"]
NON_FLAG_PARAMETERS = (
    NAME_PARAMETERS
    + PATH_PARAMETERS
    + CODE_PARAMETERS
    + BACKGROUND_PARAMETERS
    + OTHER_PARAMETERS
    + LAYOUT_PARAMETERS
)
FLAG_PARAMETERS = ["auto_start", "allow_restart", "show_sidebar", "enabled"]
DASH_PARAMETERS = FLAG_PARAMETERS + NON_FLAG_PARAMETERS


def check_valid_parameters(parameters: dict) -> None:
    for param in parameters.keys():
        if param not in DASH_PARAMETERS:
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
    return {"name": name or "New Dash"}


def evaluate_parameter_path(parameters: dict) -> dict:
    path = parameters.get("path")
    if not path:
        return {}
    return {"path": path}


def evaluate_parameters_code(parameters: dict, use_default=True) -> dict:
    code = parameters.get("code") or parameters.get("c")

    if not code:
        raise Exception("Code is required")

    return {"code_file_path": code}


def evaluate_parameter_layout(parameters: dict) -> dict:
    layout = parameters.get("layout")
    if not layout:
        raise Exception("Layout is required")
    return {"layout": layout}


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


def evaluate_other_parameters(parameters: dict) -> dict:
    other_parameters = {}
    for param, value in parameters.items():
        if param in OTHER_PARAMETERS:
            other_parameters[param] = value

    return other_parameters


def evaluate_background_parameter_value(parameters: dict) -> dict:
    background = parameters.get("background", None)
    if not background:
        return {}

    if utils.check_color(background):
        return {"theme": background}

    if not utils.path_exists(background):
        messages.file_path_does_not_exists_message(background)
        exit()

    if utils.check_is_image_path(background):
        filename = utils.slugify_filename(background)
        try:
            with open(background, "rb") as f:
                file = f.read()
                url = apis.asset_upload(filename, file)
                return {"theme": url}
        except Exception as e:
            messages.error_upload_background_message(background)
            exit()

    messages.invalid_background_parameter_value()
    exit()


class Dashes(Resource):
    @staticmethod
    def list():
        dashes = apis.list_workspace_dashes()
        messages.print_dashes(dashes)

    @staticmethod
    def add(*args, **kwargs):
        upsert = kwargs.pop("upsert", False)
        path = kwargs.get("path")
        if upsert and not path:
            messages.upsert_without_identifier("path")
            exit()

        check_valid_parameters(kwargs)

        dash_data = {
            **evaluate_parameter_name(kwargs),
            **evaluate_parameter_path(kwargs),
            **evaluate_parameters_code(kwargs),
            **evaluate_flag_parameters(kwargs),
            **evaluate_other_parameters(kwargs),
            **evaluate_background_parameter_value(kwargs),
            **evaluate_parameter_layout(kwargs),
        }

        if dash_data:
            try:
                if upsert:
                    apis.upsert_workspace_dash(dash_data)
                    messages.upserted_message("Dash", path)
                else:
                    path = apis.add_workspace_dash(dash_data)["path"]
                    messages.created_message("Dash", path)
            except Exception as e:
                print(e)
                messages.create_failed("Dash")

    @staticmethod
    def update(*args, **kwargs):
        if not len(args):
            messages.required_argument("path")
            exit()
        path = args[0]

        if not len(kwargs):
            messages.missing_parameters_to_update("dash", path)
            exit()

        check_valid_parameters(kwargs)

        dash_data = {
            **evaluate_parameter_name(kwargs, use_default=False),
            **evaluate_parameter_path(kwargs),
            **evaluate_parameters_code(kwargs, use_default=False),
            **evaluate_flag_parameters(kwargs),
            **evaluate_other_parameters(kwargs),
            **evaluate_background_parameter_value(kwargs),
            **evaluate_parameter_layout(kwargs),
        }

        if dash_data:
            try:
                apis.update_workspace_dash(path, dash_data)
                messages.updated_message("Dash", path)
            except Exception as e:
                print(e)
                messages.update_failed("Dash", path)

    @staticmethod
    def remove(*args, **kwargs):
        if not len(args):
            messages.required_argument("path")
            exit()

        path = args[0]
        apis.delete_workspace_dash(path)
        messages.deleted_message("Dash", path)

    @staticmethod
    def play(*args, **kwargs):
        if not len(args):
            messages.required_argument("path")
            exit()

        path = args[0]
        subdomain_name = apis.get_subdomain()
        url = utils.get_prod_dash_url(subdomain_name, path)
        messages.dash_url(url)
        webbrowser.open(url)

    @staticmethod
    def get_deploy_data(abstra_json_path):
        abstra_json_dir = os.path.dirname(abstra_json_path)
        with open(abstra_json_path, "r") as f:
            workspace_json_data = json.load(f)
        root_dir = workspace_json_data.get("workspace", {"root": "."})["root"]
        dash_files = glob(
            os.path.join(abstra_json_dir, root_dir, "**", "*.abstradash.json"),
            recursive=True,
        )
        dash_props = []
        for dash_file_path in dash_files:
            common_path = dash_file_path.replace(".abstradash.json", "")
            route = os.path.relpath(
                common_path, os.path.join(abstra_json_dir, root_dir)
            ).replace("\\", "/")
            script_path = common_path + ".py"
            dash_json_data = json.load(open(dash_file_path, "r"))
            prop = {
                "name": dash_json_data["name"],
                "layout": dash_json_data["layout"],
                "background": workspace_json_data["workspace"]["theme"],
                "path": route,
                "code": script_path,
            }
            dash_props.append(prop)
        return dash_props
