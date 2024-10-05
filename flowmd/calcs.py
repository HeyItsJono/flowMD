import datetime
import json
import os
import re

import requests
from bs4 import BeautifulSoup


def fetch():
    # Use soup to fetch the html
    request = requests.get("https://www.mdcalc.com/#All")
    soup = BeautifulSoup(request.content, "html.parser")

    # A json object containing a dict of all calcs, as well as some other relevant info, is stored in a script tag with the id "__NEXT_DATA__" right at the bottom of the page.
    # soup.find() returns a bs4 tag object, .contents[0] returns the actual text within that tag, but this is returned as a Script object and must be converted to a string.
    # Once it is a string, it can be converted to a nested dictionary with json.loads() making it easy to work with.
    mdcalcs = json.loads(str(soup.find("script", id="__NEXT_DATA__").contents[0]))

    # Big variables, no longer needed.
    del request, soup

    root = mdcalcs["props"]["pageProps"]["envs"]["CANONICAL_URL_ROOT"]
    raw_calcs = mdcalcs["props"]["pageProps"]["allCalcs"]
    all_calcs = []

    # Regex function that strips html tags from a string. Used for the description.
    tag_strip = re.compile(r"(<!--.*?-->|<[^>]*>)")

    for calc in raw_calcs:
        all_calcs.append(
            {
                "title": calc["full_title_en"],
                "description": tag_strip.sub("", calc["medium_description_en"]),
                "url": root + "/calc/" + str(calc["id"]) + "/" + calc["slug"],
            }
        )

    # Big variables, no longer needed.
    del raw_calcs, mdcalcs
    return all_calcs


def cache(age=7):
    # Check for the existence of a cache file. If it exists, check if it was generated less than 'age' days ago (default = 1wk). If it was, return the cached calcs.
    cache_file = "cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)
            if datetime.datetime.now() - datetime.datetime.fromisoformat(
                cache["timestamp"]
            ) < datetime.timedelta(days=age):
                return cache["calcs"]

    # If the cache file doesn't exist, or is older than a week, fetch the calcs, write them to the cache file, and return them.
    calcs = fetch()
    with open(cache_file, "w") as f:
        json.dump(
            {"calcs": calcs, "timestamp": str(datetime.datetime.now().isoformat())}, f
        )
    return calcs


if __name__ == "__main__":
    print(cache())
