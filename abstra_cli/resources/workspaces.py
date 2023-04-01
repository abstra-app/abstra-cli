import json

from abstra_cli import messages
from abstra_cli.utils import parse_timestamp, sampling
from abstra_cli.resources.resources import Resource
from abstra_cli.apis import (
    jobs as jobs_api,
    hooks as hooks_api,
    forms as forms_api,
    dashes as dashes_api,
)


class Workspaces(Resource):
    @staticmethod
    def logs(*args, **kwargs):
        limit = kwargs.get("limit", None)
        offset = kwargs.get("offset", 0)

        job_logs = jobs_api.list_logs(limit, offset)["logs"]
        hook_logs = hooks_api.list_logs(limit, offset)["logs"]
        form_logs = forms_api.list_logs(limit, offset)["logs"]
        dash_logs = dashes_api.list_logs(limit, offset)["logs"]

        logs = job_logs + hook_logs + form_logs + dash_logs
        logs.sort(key=lambda x: parse_timestamp(x["created_at"]), reverse=True)
        logs = sampling(logs, limit, offset)
        serialized_logs = json.dumps(logs, default=str, indent=4)
        messages.print_logs(serialized_logs)
