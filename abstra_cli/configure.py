from .utils_config import save_config


def configure(api_token):
    save_config({'api_token': api_token})
    print("Done!")
