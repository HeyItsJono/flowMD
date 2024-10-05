import json
import os
import sys

DEFAULT_SETTINGS = {"age": "7", "favourites": []}


def get():
    # json.loads(sys.argv[1])
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            settings = json.load(f)
        return settings
    else:
        with open("settings.json", "w") as f:
            json.dump(DEFAULT_SETTINGS, f)
        return DEFAULT_SETTINGS


def save(settings):
    rpc_settings_request = {"method": "", "parameters": [], "settings": settings}
    json.dump(rpc_settings_request, sys.stdout)
    with open("settings.json", "w") as f:
        json.dump(settings, f)

    return


if __name__ == "__main__":
    get()
