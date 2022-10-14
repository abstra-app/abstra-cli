from webbrowser import open

from abstra_cli.resources.resources import Resource
from ..apis import (
    add_workspace_form,
    list_workspace_forms,
    delete_workspace_form,
    update_workspace_form,
    asset_upload,
    get_subdomain_by_form_id,
)
from ..cli_helpers import print_forms
from ..messages import (
    code_and_file_not_allowed,
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
)

from ..utils import (
    check_color,
    check_is_image_path,
    slugify_filename,
    path_exists,
    get_prod_form_url,
)

NAME_PARAMETERS = ["name"]
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
    NAME_PARAMETERS + CODE_PARAMETERS + BACKGROUND_PARAMETERS + OTHER_PARAMETERS
)

FORM_PARAMETERS = FLAG_PARAMETERS + NON_FLAG_PARAMETERS


def evaluate_parameter_name(parameters, form_data: dict) -> dict:
    name = parameters.get("name") or parameters.get("n")
    if not name:
        required_parameter("name")
        exit()

    form_data["name"] = name
    return form_data


def add_parameters_file_and_code(parameters: dict, form_data: dict) -> dict:
    EMPTY_FORM = "from hackerforms import *"
    file = parameters.get("file") or parameters.get("f")
    code = parameters.get("code") or parameters.get("c")

    if file and code:
        code_and_file_not_allowed()
        exit()

    if file:
        with open(file, "r") as f:
            form_data["code"] = f.read()
            return form_data

    if code:
        form_data["code"] = code
        return form_data

    form_data["code"] = EMPTY_FORM
    return form_data


def update_parameters_file_and_code(parameters, form_data):
    file = parameters.get("file") or parameters.get("f")
    code = parameters.get("code") or parameters.get("c")

    if file and code:
        code_and_file_not_allowed()
        exit()

    if file:
        with open(file, "r") as f:
            form_data["code"] = f.read()

    if code:
        form_data["code"] = code

    return form_data


def build_other_parameters(parameters, form_data, valid_parameters):
    for param, value in parameters.items():
        if param in valid_parameters:
            form_data[param] = value

    return form_data


def check_valid_parameters(parameters, valid_parameters):
    for param in parameters.keys():
        if param not in valid_parameters:
            invalid_parameter(param)
            exit()


def evaluate_non_flag_parameters_values(parameters, form_data, non_flag_parameters):
    for param, value in parameters.items():
        if param in non_flag_parameters and value in [True, False]:
            invalid_non_flag_parameter_value(param)
            exit()

    return form_data


def evaluate_flag_parameters(parameters, form_data, flag_parameters):
    for param, value in parameters.items():
        if param in flag_parameters:
            if value == "true" or value == True:
                form_data[param] = True
                continue
            if value == "false" or value == False:
                form_data[param] = False
                continue

            invalid_flag_parameter_value(param)
            exit()

    return form_data


def evaluate_background_parameter_value(parameters: dict, form_data: dict):
    background = parameters.get("background", None)
    if not background:
        return

    if check_color(background):
        form_data["theme"] = background
        return form_data

    if not path_exists(background):
        file_path_does_not_exists_message(background)
        exit()

    if check_is_image_path(background):
        filename = slugify_filename(background)
        try:
            with open(background, "rb") as f:
                file = f.read()
                url = asset_upload(filename, file)
                form_data["theme"] = url
                return form_data
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
        form_data = {}
        check_valid_parameters(kwargs, FORM_PARAMETERS)
        form_data = evaluate_parameter_name(kwargs, form_data.copy())
        form_data = add_parameters_file_and_code(kwargs, form_data.copy())
        form_data = evaluate_background_parameter_value(kwargs, form_data.copy())
        form_data = evaluate_flag_parameters(kwargs, form_data.copy(), FLAG_PARAMETERS)
        form_data = evaluate_non_flag_parameters_values(
            kwargs, form_data.copy(), NON_FLAG_PARAMETERS
        )
        form_data = build_other_parameters(kwargs, form_data.copy(), OTHER_PARAMETERS)
        form_id = add_workspace_form(form_data)["id"]
        form_created_message(form_id)

    @staticmethod
    def update(*args, **kwargs):

        if not len(args):
            required_argument("form_id")
            exit()

        form_id = args[0]
        if not len(kwargs):
            missing_parameters_to_update(form_id)
            exit()

        form_data = {}
        check_valid_parameters(kwargs, FORM_PARAMETERS)
        form_data = update_parameters_file_and_code(kwargs, form_data.copy())
        form_data = evaluate_background_parameter_value(kwargs, form_data.copy())
        form_data = evaluate_flag_parameters(kwargs, form_data.copy(), FLAG_PARAMETERS)
        form_data = evaluate_non_flag_parameters_values(
            kwargs, form_data.copy(), NON_FLAG_PARAMETERS
        )
        form_data = build_other_parameters(
            kwargs, form_data.copy(), OTHER_PARAMETERS + NAME_PARAMETERS
        )
        update_workspace_form(form_id, form_data)
        form_updated_message(form_id)

    @staticmethod
    def remove(*args, **kwargs):
        if not len(args):
            required_argument("form_id")
            exit()
        form_id = args[0]
        delete_workspace_form(form_id)

    @staticmethod
    def play(*args, **kwargs):
        if not len(args):
            required_argument("form_id")
            exit()
        form_id = args[0]
        response = get_subdomain_by_form_id(form_id)
        if not len(response):
            print(
                "There is no workspace related to this form id. Please, verify whether it is correct."
            )
            exit()
        subdomain_name = response[0]["name"]
        url = get_prod_form_url(subdomain_name, form_id)
        open(url)
