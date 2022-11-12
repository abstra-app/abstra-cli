import webbrowser


from abstra_cli.resources.resources import Resource
import abstra_cli.cli_helpers as cli_helpers
import abstra_cli.messages as messages
import abstra_cli.utils as utils
import abstra_cli.apis as apis


NAME_PARAMETERS = ["name", "title"]
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
            messages.invalid_parameter(param)
            exit()
    for param, value in parameters.items():
        if param in NON_FLAG_PARAMETERS and value in [True, False]:
            messages.invalid_non_flag_parameter_value(param)
            exit()


def evaluate_parameter_name(parameters: dict) -> dict:
    name = (
        parameters.get("name")
        or parameters.get("n")
        or parameters.get("title")
        or "New Form"
    )
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
        messages.code_and_file_not_allowed()
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

            messages.invalid_flag_parameter_value(param)
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


class Forms(Resource):
    @staticmethod
    def list():
        forms = apis.list_workspace_forms()
        cli_helpers.print_forms(forms)

    @staticmethod
    def add(*args, **kwargs):
        upsert = kwargs.pop('upsert', False)
        path = kwargs.get('path')
        if upsert and not path:
            messages.upsert_without_identifier("path")
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
                if upsert:
                    apis.upsert_workspace_form(form_data)
                    messages.form_upserted_message(path)
                else:
                    path = apis.add_workspace_form(form_data)["path"]
                    messages.form_created_message(path)
            except Exception as e:
                print(e)
                messages.form_create_failed()

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
                apis.update_workspace_form(path, form_data)
                messages.form_updated_message(path)
            except Exception as e:
                print(e)
                messages.form_update_failed(path)

    @staticmethod
    def remove(*args, **kwargs):
        if not len(args):
            messages.required_argument("path")
            exit()

        path = args[0]
        apis.delete_workspace_form(path)
        messages.form_deleted_message(path)

    @staticmethod
    def play(*args, **kwargs):
        if not len(args):
            messages.required_argument("path")
            exit()

        path = args[0]
        subdomain_name = apis.get_subdomain()
        url = utils.get_prod_form_url(subdomain_name, path)
        messages.form_url(url)
        webbrowser.open(url)
