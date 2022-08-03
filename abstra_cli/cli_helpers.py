from progress.bar import FillingSquaresBar

from .utils import format_digits


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


def print_file(file, max_d):
    print(
        f"{format_digits(file['Size'], max_d)} - {file['LastModified']}: {file['Key']}"
    )


def print_var(var):
    print(f"{var['name']}={var['value']}")


def print_package(pkg):
    print(f"{pkg['name']}{'==' + pkg['version'] if pkg['version'] else ''}")
