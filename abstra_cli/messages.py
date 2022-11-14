def created_message(resource: str, form: str):
    print(f"{resource} created successfully: {form}")


def upserted_message(resource: str, form: str):
    print(f"{resource} upserted successfully: {form}")


def create_failed(resource: str):
    print(f"Failed to create {resource}")


def updated_message(resource: str, form: str):
    print(f"{resource} updated successfully: {form}")


def deleted_message(resource: str, form: str):
    print(f"{resource} deleted successfully: {form}")


def update_failed(resource: str, form: str):
    print(f"Failed to update {resource}: {form}")


def not_implemented(*args, **kwargs):
    print("Invalid command")


def required_argument(argument):
    print(f"required argument: [{argument}]")


def required_parameter(parameter):
    print(f"required parameter: --{parameter} [{parameter}]")


def invalid_variable(argument):
    print(f"invalid variable: {argument}")


def invalid_parameter(parameter):
    print(f"invalid parameter: --{parameter} [{parameter}]")


def invalid_flag_parameter_value(parameter):
    print(
        f"invalid parameter value: --{parameter} [{parameter}] value must be true or false"
    )


def invalid_non_flag_parameter_value(parameter):
    print(f"invalid parameter value: --{parameter} [{parameter}] value must be string")


def invalid_background_parameter_value():
    print(
        f"""
        invalid parameter value: --background [background] value must be a color or image path.\n
        Allowed image extensions are: [.png, .jpeg, .jpg, .svg]"""
    )


def duplicate_variable(argument):
    print(f"duplicate variable: {argument}")


def code_and_file_not_allowed():
    print("you can set either code or file parameters, but not both.")


def missing_parameters_to_update(form):
    print(f"missing parameters to be updated of form {form}")


def file_path_does_not_exists_message(path):
    print(f"file path not found: {path}")


def upsert_without_identifier(idt):
    print(f"Failed to upsert without identifier: {idt}")


def error_upload_background_message(path):
    print(f"Some error happened during background upload: {path}")


def form_url(url):
    print(f"Opening URL {url}")


def hook_url(url, method):
    print(f"Making {method} request to URL {url}")
