import webbrowser

from flowlauncher import FlowLauncher

import plugin.calcs
import plugin.settings

calcs = plugin.calcs.cache()
settings = plugin.settings.get()


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
                        "ContextData": calc,
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
                            "ContextData": calc,
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

    def context_menu(self, calc):
        # "calc" in this case is passed to this function via the ContextData from the query results.
        return [
            {
                "Title": "Open Calculator",
                "SubTitle": "Open the calculator in the default browser.",
                "IcoPath": "assets/mdcalc.png",
                "JSONRPCAction": {
                    "method": "open_url",
                    "parameters": [calc["url"]],
                },
            },
            {
                "Title": "Add to Favourites",
                "SubTitle": "Favourite calculators are shown above the others.",
                "IcoPath": "assets/mdcalc.png",
                "JSONRPCAction": {
                    "method": "add_to_favourites",
                    "parameters": [calc["title"]],
                },
            },
        ]

    def open_url(self, url):
        webbrowser.open(url)
        return

    def add_to_favourites(self, title):
        settings["favourites"].append(title)
        plugin.settings.save(settings)
        return


if __name__ == "__main__":
    flowMD()
