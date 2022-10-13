def form_created_message(form_id: str):
    print(f"Form created successfully: {form_id}")


def form_updated_message(form_id: str):
    print(f"Form updated successfully: {form_id}")


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


def duplicate_variable(argument):
    print(f"duplicate variable: {argument}")


def code_and_file_not_allowed():
    print("you can set either code or file parameters, but not both.")


def missing_parameters_to_update(form_id):
    print(f"missing parameters to be updated of form {form_id}")
