from progress.bar import FillingSquaresBar


def read_credentials():
    print(
        "Abstra API Tokens can be found in your workspace or at https://forms.abstra.run/737986ce-a8ed-4c7b-bd7e-5f0b11331b66."
    )
    credentials = input(f"API Token: ")
    if not credentials:
        raise Exception("No API token configured")
    return credentials


def show_progress(message, max):
    return FillingSquaresBar(message, suffix="%(percent)d%%", max=max)
