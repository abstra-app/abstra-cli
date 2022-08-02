def read_api_token():
    print(
        "Abstra API Tokens can be found in your workspace or at https://forms.abstra.run/737986ce-a8ed-4c7b-bd7e-5f0b11331b66."
    )
    api_token = input(f"API Token: ")
    if not api_token:
        raise Exception("No API token configured")
    return api_token
