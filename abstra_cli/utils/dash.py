from . import parse_timestamp


def flat_dash_logs(dashes):
    """Ungroup dashes from the response of the list_logs query."""
    logs = []
    for dash in dashes:
        current_logs = dash.get("logs")
        for log in current_logs:
            log["path"] = dash.get("path")
            logs.append(log)

    logs.sort(key=lambda x: parse_timestamp(x["created_at"]), reverse=True)
    return logs
