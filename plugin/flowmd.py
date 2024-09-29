import webbrowser

from flowlauncher import FlowLauncher

import plugin.calcs

calcs = plugin.calcs.cache()
settings = plugin.SETTINGS


class flowMD(FlowLauncher):
    def query(self, query):
        results = []
        if query == "":
            for calc in calcs:
                if any(fav in calc["title"] for fav in settings["favourites"]):
                    score = 100
                else:
                    score = 0
                results.append(
                    {
                        "Title": calc["title"],
                        "SubTitle": calc["description"],
                        "IcoPath": "assets/mdcalc.png",
                        "JSONRPCAction": {
                            "method": "open_url",
                            "parameters": [calc["url"]],
                        },
                        "score": score,
                    }
                )
        elif len(query) > 0:
            for calc in calcs:
                if any(fav in calc["title"] for fav in settings["favourites"]):
                    score = 100
                else:
                    score = 0
                if (
                    query in calc["title"].lower()
                    or query in calc["description"].lower()
                ):
                    results.append(
                        {
                            "Title": calc["title"],
                            "SubTitle": calc["description"],
                            "IcoPath": "assets/mdcalc.png",
                            "JSONRPCAction": {
                                "method": "open_url",
                                "parameters": [calc["url"]],
                            },
                            "score": score,
                        }
                    )
        if not results:
            results.append(
                {
                    "Title": "No results found",
                    "SubTitle": "Try searching for something else.",
                    "IcoPath": "assets/mdcalc.png",
                }
            )
        return results

    def context_menu(self, data):
        return [
            {
                "Title": "Open Calculator",
                "SubTitle": "Open the calculator in the default browser.",
                "IcoPath": "assets/mdcalc.png",
                "JSONRPCAction": {
                    "method": "open_url",
                    "parameters": [data["JSONRPCAction"]["parameters"][0]],
                },
            },
            {
                "Title": "Add to Favourites",
                "SubTitle": "(WIP) Favourite calculators are shown above the others.",
                "IcoPath": "assets/mdcalc.png",
                "JSONRPCAction": {
                    "method": "add_to_favourites",
                    "parameters": [data["Title"]],
                },
            },
        ]

    def open_url(self, url):
        webbrowser.open(url)
        return

    def add_to_favourites(self, title):
        settings["favourites"].append(title)
        plugin.saveSettings(settings)
        return


if __name__ == "__main__":
    flowMD()
