from progress.bar import FillingSquaresBar

from .utils import digits, format_digits


def read_credentials():
    print(
        "Abstra API Tokens can be found in your workspace or at https://forms.abstra.run/737986ce-a8ed-4c7b-bd7e-5f0b11331b66."
    )
    credentials = input(f"API Token: ")
    if not credentials:
        raise Exception("No API token configured")
    return credentials


def show_progress(message, max) -> FillingSquaresBar:
    return FillingSquaresBar(message, suffix="%(percent)d%%", max=max)

def print_files(files):
    files.sort(key=lambda x: x["Key"])
    max_d = digits(max([f["Size"] for f in files]))
    for file in files:
        print(
            f"{format_digits(file['Size'], max_d)} - {file['LastModified']}: {file['Key']}"
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
    forms.sort(key=lambda x: x["title"])
    max_d = max([len(f["path"]) for f in forms])
    for form in forms:
        print(f"{format_digits(form['path'], max_d)} - {form['title']}")
