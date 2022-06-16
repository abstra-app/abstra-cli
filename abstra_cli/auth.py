import requests

from .utils import read_user_config, save_user_config


def refresh_config():
    config = read_user_config()
    # { client_id, authority, access_token, refresh_token }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": config["refresh_token"],
        "client_id": config["client_id"]
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(config["authority"] +
                      "/oauth/token", data=data, headers=headers)

    new_tokens = r.json()
    save_user_config({
        **config,
        'access_token': new_tokens['access_token'],
        'refresh_token': new_tokens['refresh_token']
    })

    return read_user_config()
