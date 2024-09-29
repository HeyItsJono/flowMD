import json
import os

# from typing import Literal, TypedDict
# Settings = TypedDict("Settings", {"age": Literal["1", "3", "5", "7", "10", "14", "21"],
# 	'favourites': str | None})


DEFAULT_SETTINGS = {"age": "7", "favourites": []}


def getSettings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            SETTINGS = json.load(f)
        return SETTINGS
    else:
        with open("settings.json", "w") as f:
            json.dump(DEFAULT_SETTINGS, f)
        return DEFAULT_SETTINGS


def saveSettings(SETTINGS):
    with open("settings.json", "w") as f:
        json.dump(SETTINGS, f)
    return


if __name__ == "__main__":
    getSettings()
