import webbrowser

from abstra_cli.resources.resources import Resource
from ..apis import (
    add_workspace_form,
    list_workspace_forms,
    delete_workspace_form,
    update_workspace_form,
    asset_upload,
    get_subdomain,
)
from ..cli_helpers import print_forms
from ..messages import (
    code_and_file_not_allowed,
    form_deleted_message,
    invalid_parameter,
    required_argument,
    required_parameter,
    invalid_flag_parameter_value,
    invalid_non_flag_parameter_value,
    missing_parameters_to_update,
    invalid_background_parameter_value,
    file_path_does_not_exists_message,
    error_upload_background_message,
    form_created_message,
    form_updated_message,
    form_create_failed,
    form_update_failed,
    form_url,
)

from ..utils import (
    check_color,
    check_is_image_path,
    slugify_filename,
    path_exists,
    get_prod_form_url,
)

NAME_PARAMETERS = ["name"]
PATH_PARAMETERS = ["path"]
CODE_PARAMETERS = ["file", "f", "code", "c"]
BACKGROUND_PARAMETERS = ["background"]
FLAG_PARAMETERS = ["auto_start", "allow_restart", "show_sidebar"]
OTHER_PARAMETERS = [
    "start_message",
    "end_message",
    "error_message",
    "timeout_mesage",
    "main_color",
    "start_button_text",
    "logo_url",
    "log_messages",
    "font_color",
    "welcome_title",
    "brand_name",
]
NON_FLAG_PARAMETERS = (
    NAME_PARAMETERS
    + PATH_PARAMETERS
    + CODE_PARAMETERS
    + BACKGROUND_PARAMETERS
    + OTHER_PARAMETERS
)

FORM_PARAMETERS = FLAG_PARAMETERS + NON_FLAG_PARAMETERS


def check_valid_parameters(parameters):
    for param in parameters.keys():
        if param not in FORM_PARAMETERS:
            invalid_parameter(param)
            exit()
    for param, value in parameters.items():
        if param in NON_FLAG_PARAMETERS and value in [True, False]:
            invalid_non_flag_parameter_value(param)
            exit()


def evaluate_parameter_name(parameters: dict) -> dict:
    name = parameters.get("name") or parameters.get("n") or "New Form"
    return {"name": name}


def evaluate_parameter_path(parameters: dict) -> dict:
    path = parameters.get("path")
    if not path:
        return {}
    return {"path": path}


def evaluate_parameters_file_and_code(parameters: dict) -> dict:
    EMPTY_FORM = "from hackerforms import *"
    file = parameters.get("file") or parameters.get("f")
    code = parameters.get("code") or parameters.get("c")

    if file and code:
        code_and_file_not_allowed()
        exit()

    if file:
        with open(file, "r") as f:
            return {"code": f.read()}

    if code:
        return {"code": code}

    return {"code": EMPTY_FORM}


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

            invalid_flag_parameter_value(param)
            exit()

    return evaluated_params


def evaluate_other_parameters(parameters) -> dict:
    other_parameters = {}
    for param, value in parameters.items():
        if param in OTHER_PARAMETERS:
            other_parameters[param] = value

    return other_parameters


def evaluate_background_parameter_value(parameters: dict) -> dict:
    background = parameters.get("background", None)
    if not background:
        return {}

    if check_color(background):
        return {"theme": background}

    if not path_exists(background):
        file_path_does_not_exists_message(background)
        exit()

    if check_is_image_path(background):
        filename = slugify_filename(background)
        try:
            with open(background, "rb") as f:
                file = f.read()
                url = asset_upload(filename, file)
                return {"theme": url}
        except Exception as e:
            error_upload_background_message(background)
            exit()

    invalid_background_parameter_value()
    exit()


class Forms(Resource):
    @staticmethod
    def list():
        forms = list_workspace_forms()
        print_forms(forms)

    @staticmethod
    def add(*args, **kwargs):
        check_valid_parameters(kwargs)

        form_data = {
            **evaluate_parameter_name(kwargs),
            **evaluate_parameter_path(kwargs),
            **evaluate_parameters_file_and_code(kwargs),
            **evaluate_flag_parameters(kwargs),
            **evaluate_other_parameters(kwargs),
            **evaluate_background_parameter_value(kwargs),
        }

        if form_data:
            try:
                path = add_workspace_form(form_data)["path"]
                form_created_message(path)
            except:
                form_create_failed()

    @staticmethod
    def update(*args, **kwargs):

        if not len(args):
            required_argument("path")
            exit()
        path = args[0]

        if not len(kwargs):
            missing_parameters_to_update(path)
            exit()

        check_valid_parameters(kwargs)

        form_data = {
            **evaluate_parameter_name(kwargs),
            **evaluate_parameter_path(kwargs),
            **evaluate_parameters_file_and_code(kwargs),
            **evaluate_flag_parameters(kwargs),
            **evaluate_other_parameters(kwargs),
            **evaluate_background_parameter_value(kwargs),
        }

        if form_data:
            try:
                update_workspace_form(path, form_data)
                form_updated_message(path)
            except:
                form_update_failed(path)

    @staticmethod
    def remove(*args, **kwargs):
        if not len(args):
            required_argument("path")
            exit()

        path = args[0]
        delete_workspace_form(path)
        form_deleted_message(path)

    @staticmethod
    def play(*args, **kwargs):
        if not len(args):
            required_argument("path")
            exit()

        path = args[0]
        subdomain_name = get_subdomain()
        url = get_prod_form_url(subdomain_name, path)
        form_url(url)
        webbrowser.open(url)
