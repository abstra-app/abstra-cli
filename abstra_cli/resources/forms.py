from abstra_cli.resources.resources import Resource
from ..apis import (
    add_workspace_form,
    list_workspace_forms,
    delete_workspace_form,
    update_workspace_form,
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


def evaluate_parameter_name(parameters, form_data):
    name = parameters.get("name") or parameters.get("n")
    if not name:
        required_parameter("name")
        exit()

    form_data["name"] = name
    return form_data


def evaluate_parameters_file_and_code(parameters, form_data):
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


class Forms(Resource):
    @staticmethod
    def list(*args, **kwargs):
        forms = list_workspace_forms()
        print_forms(forms)

    @staticmethod
    def add(*args, **kwargs):
        form_data = {}
        check_valid_parameters(kwargs, FORM_PARAMETERS)
        form_data = evaluate_parameter_name(kwargs, form_data.copy())
        form_data = evaluate_parameters_file_and_code(kwargs, form_data.copy())
        form_data = evaluate_flag_parameters(kwargs, form_data.copy(), FLAG_PARAMETERS)
        form_data = evaluate_non_flag_parameters_values(
            kwargs, form_data.copy(), NON_FLAG_PARAMETERS
        )
        form_data = build_other_parameters(kwargs, form_data.copy(), OTHER_PARAMETERS)
        add_workspace_form(form_data)

    @staticmethod
    def update(*args, **kwargs):
        form_id = args[0]

        if not form_id:
            required_argument("form_id")
            exit()

        if not len(kwargs):
            missing_parameters_to_update(form_id)
            exit()

        form_data = {}
        check_valid_parameters(kwargs, FORM_PARAMETERS)
        form_data = update_parameters_file_and_code(kwargs, form_data.copy())
        form_data = evaluate_flag_parameters(kwargs, form_data.copy(), FLAG_PARAMETERS)
        form_data = evaluate_non_flag_parameters_values(
            kwargs, form_data.copy(), NON_FLAG_PARAMETERS
        )
        form_data = build_other_parameters(
            kwargs, form_data.copy(), OTHER_PARAMETERS + NAME_PARAMETERS
        )
        update_workspace_form(form_id, form_data)

    @staticmethod
    def remove(*args, **kwargs):
        form_id = args[0]
        if not form_id:
            required_argument("form_id")
            exit()
        delete_workspace_form(args[0])
