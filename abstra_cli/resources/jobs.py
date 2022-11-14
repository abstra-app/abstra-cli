import requests
from crontab import CronTab

from abstra_cli.resources.resources import Resource
import abstra_cli.cli_helpers as cli_helpers
import abstra_cli.messages as messages
import abstra_cli.utils as utils
import abstra_cli.apis as apis


NAME_PARAMETERS = ["name", "title"]
IDT_PARAMETERS = ["identifier", "idt"]
CODE_PARAMETERS = ["file", "f", "code", "c"]
SCHEDULE_PARAMETERS = ["schedule", "crontab"]
NON_FLAG_PARAMETERS = (
    NAME_PARAMETERS + IDT_PARAMETERS + CODE_PARAMETERS + SCHEDULE_PARAMETERS
)
FLAG_PARAMETERS = ["enabled"]
JOB_PARAMETERS = FLAG_PARAMETERS + NON_FLAG_PARAMETERS


def check_valid_parameters(parameters: dict) -> None:
    for param in parameters.keys():
        if param not in JOB_PARAMETERS:
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
    return {"name": name or "New Job"}


def evaluate_parameter_idt(parameters: dict) -> dict:
    identifier = parameters.get("idt") or parameters.get("identifier")
    if not identifier:
        return {}
    return {"identifier": identifier}


def evaluate_parameter_schedule(parameters: dict, use_default=True) -> dict:
    schedule = parameters.get("schedule") or parameters.get("crontab")
    if schedule:
        try:
            CronTab(schedule)
            return {"schedule": schedule}
        except:
            print("Bad crontab expression")
            exit()

    return {"schedule": "00 00 00 * *"} if use_default else {}


def evaluate_parameters_file_and_code(parameters: dict, use_default=True) -> dict:
    EMPTY_JOB = "print('Done!')"
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

    return {"code": EMPTY_JOB} if use_default else {}


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


class Jobs(Resource):
    @staticmethod
    def list():
        jobs = apis.list_workspace_jobs()
        cli_helpers.print_jobs(jobs)

    @staticmethod
    def add(*args, **kwargs):
        upsert = kwargs.pop("upsert", False)
        idt = evaluate_parameter_idt(kwargs).get("identifier")
        if upsert and not idt:
            messages.upsert_without_identifier("identifier")
            exit()

        check_valid_parameters(kwargs)

        job_data = {
            **evaluate_parameter_name(kwargs),
            **evaluate_parameter_idt(kwargs),
            **evaluate_parameter_schedule(kwargs),
            **evaluate_parameters_file_and_code(kwargs),
            **evaluate_flag_parameters(kwargs),
        }

        if job_data:
            try:
                if upsert:
                    apis.upsert_workspace_job(job_data)
                    messages.upserted_message("Job", idt)
                else:
                    idt = apis.add_workspace_job(job_data)["identifier"]
                    messages.created_message("Job", idt)
            except Exception as e:
                print(e)
                messages.create_failed(
                    "Job",
                )

    @staticmethod
    def update(*args, **kwargs):

        if not len(args):
            messages.required_argument("identifier")
            exit()
        idt = args[0]

        if not len(kwargs):
            messages.missing_parameters_to_update(idt)
            exit()

        check_valid_parameters(kwargs)

        job_data = {
            **evaluate_parameter_name(kwargs, use_default=False),
            **evaluate_parameter_idt(kwargs),
            **evaluate_parameter_schedule(kwargs, use_default=False),
            **evaluate_parameters_file_and_code(kwargs, use_default=False),
            **evaluate_flag_parameters(kwargs),
        }

        if job_data:
            try:
                apis.update_workspace_job(idt, job_data)
                messages.updated_message("Job", idt)
            except Exception as e:
                print(e)
                messages.update_failed("Job", idt)

    @staticmethod
    def remove(*args, **kwargs):
        if not len(args):
            messages.required_argument("identifier")
            exit()

        idt = args[0]
        apis.delete_workspace_job(idt)
        messages.deleted_message("Job", idt)