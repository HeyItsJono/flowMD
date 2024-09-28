import webbrowser

from flowlauncher import FlowLauncher

import plugin.calcs

calcs = plugin.calcs.fetch()


class flowMD(FlowLauncher):
    def query(self, query):
        results = []
        if query == "":
            for calc in calcs:
                results.append(
                    {
                        "Title": calc["title"],
                        "SubTitle": calc["description"],
                        "IcoPath": "assets/mdcalc.png",
                        "JSONRPCAction": {
                            "method": "open_url",
                            "parameters": [calc["url"]],
                        },
                    }
                )
        elif len(query) > 0:
            for calc in calcs:
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
                "Title": "Add to Favourites",
                "SubTitle": "Favourite calculators are shown above the others.",
                "IcoPath": "assets/mdcalc.png",
                "JSONRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://www.mdcalc.com/"],
                },
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    flowMD()
