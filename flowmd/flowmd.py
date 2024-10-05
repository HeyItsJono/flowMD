import webbrowser

from pyflowlauncher import Plugin, Result, send_results
from pyflowlauncher.result import ResultResponse

from flowmd.calcs import cache

flowMD = Plugin()
cache_age = flowMD.settings.get("age")
favourites = flowMD.settings.get("favourites").split("\r\n")
calcs = cache(cache_age)


def check_faves(title: str) -> int:
    if any(fav in title for fav in favourites):
        return 100
    else:
        return 0


def open_url(url: str):
    webbrowser.open(url)
    return


@flowMD.on_method
def query(query: str) -> ResultResponse:
    results = []
    if len(query) > 0:
        for calc in calcs:
            if query in calc["title"].lower() or query in calc["description"].lower():
                results.append(
                    Result(
                        Title=calc["title"],
                        SubTitle=calc["description"],
                        IcoPath="assets/mdcalc.png",
                        ContextData=calc,
                        Score=check_faves(calc["title"]),
                        JsonRPCAction={
                            "method": "open_url",
                            "parameters": [calc["url"]],
                        },
                    )
                )
    else:
        for calc in calcs:
            results.append(
                Result(
                    Title=calc["title"],
                    SubTitle=calc["description"],
                    IcoPath="assets/mdcalc.png",
                    ContextData=calc,
                    Score=check_faves(calc["title"]),
                    JsonRPCAction={
                        "method": "open_url",
                        "parameters": [calc["url"]],
                    },
                )
            )

    if not results:
        results.append(
            Result(
                Title="No results found",
                SubTitle="Try searching for something else.",
                IcoPath="assets/mdcalc.png",
            )
        )
    return send_results(results)


@flowMD.on_method
def context_menu(calc):
    # "calc" in this case is passed to this function via the ContextData from the query results.
    if check_faves(calc["title"]) == 0:
        toggle_favourites = Result(
            Title="Add to Favourites",
            SubTitle="Favourite calculators are shown above the others.",
            IcoPath="assets/mdcalc.png",
            JSONRPCAction={
                "method": "add_fav",
                "parameters": [calc["title"]],
            },
        )
    else:
        toggle_favourites = Result(
            Title="Remove from Favourites",
            SubTitle="Favourite calculators are shown above the others.",
            IcoPath="assets/mdcalc.png",
            JSONRPCAction={
                "method": "remove_fav",
                "parameters": [calc["title"]],
            },
        )

    return send_results(
        [
            Result(
                Title="Open Calculator",
                SubTitle="Open the calculator in the default browser.",
                IcoPath="assets/mdcalc.png",
                JSONRPCAction={
                    "method": "open_url",
                    "parameters": [calc["url"]],
                },
            ),
            toggle_favourites,
        ]
    )


@flowMD.on_method
def add_fav(title: str):
    favourites.append(title)
    send_results(
        results=Result(),
        settings={
            "age": cache_age,
            "favourites": "\r\n".join(favourites),
            "textInput": None,
        },
    )
    return


@flowMD.on_method
def remove_fav(title: str):
    favourites.remove(title)
    send_results(
        results=Result(),
        settings={
            "age": cache_age,
            "favourites": "\r\n".join(favourites),
            "textInput": None,
        },
    )
    return


if __name__ == "__main__":
    flowMD.run()
