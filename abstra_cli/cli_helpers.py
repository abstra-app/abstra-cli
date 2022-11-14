from progress.bar import FillingSquaresBar

import abstra_cli.utils as utils


def read_credentials():
    print(
        "Abstra API Tokens can be found in your workspace or at https://forms.abstra.run/generate-token."
    )
    credentials = input(f"API Token: ")
    if not credentials:
        raise Exception("No API token configured")
    return credentials


def show_progress(message, max) -> FillingSquaresBar:
    return FillingSquaresBar(message, suffix="%(percent)d%%", max=max)


def print_files(files):
    files.sort(key=lambda x: x["Key"])
    max_d = utils.digits(max([f["Size"] for f in files]))
    for file in files:
        print(
            f"{utils.format_digits(file['Size'], max_d)} - {file['LastModified']}: {file['Key']}"
        )


def print_vars(vars):
    vars.sort(key=lambda x: x["name"])
    for var in vars:
        print(f"{var['name']}={var['value']}")


def print_packages(packages):
    packages.sort(key=lambda x: x["name"])
    for pkg in packages:
        print(f"{pkg['name']}{'==' + pkg['version'] if pkg['version'] else ''}")


def print_forms(forms):
    forms.sort(key=lambda x: x["path"])
    max_path = max([len(f["path"]) for f in forms])
    max_title = max([len(f["title"]) for f in forms])
    for form in forms:
        enabled = "enabled" if form["script"]["enabled"] else "disabled"
        print(
            f"{utils.format_digits(form['path'], max_path)} - {utils.format_digits(form['title'], max_title)} ({enabled})"
        )


def print_hooks(hooks):
    hooks.sort(key=lambda x: x["path"])
    max_path = max([len(f["path"]) for f in hooks])
    max_title = max([len(f["title"]) for f in hooks])
    for form in hooks:
        enabled = "enabled" if form["script"]["enabled"] else "disabled"
        print(
            f"{utils.format_digits(form['path'], max_path)} - {utils.format_digits(form['title'], max_title)} ({enabled})"
        )


def print_jobs(jobs):
    jobs.sort(key=lambda x: x["identifier"])
    max_idt = max([len(f["identifier"]) for f in jobs])
    max_title = max([len(f["title"]) for f in jobs])
    max_schedule = max([len(f["schedule"]) for f in jobs])
    for j in jobs:
        enabled = "enabled" if j["script"]["enabled"] else "disabled"
        print(
            f"{utils.format_digits(j['identifier'], max_idt)} - {utils.format_digits(j['schedule'], max_schedule)} - {utils.format_digits(j['title'], max_title)} ({enabled})"
        )
