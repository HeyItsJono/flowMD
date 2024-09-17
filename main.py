import sys
from pathlib import Path

# Bootstrap code for the FlowLauncher plugin to allow for importing of external modules.
plugindir = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "plugin")
sys.path = [str(plugindir / p) for p in paths] + sys.path

import webbrowser  # noqa: E402

from flowlauncher import FlowLauncher  # noqa: E402

import calcs  # noqa: E402

calcs = calcs.fetch()


class MDCalc(FlowLauncher):
    def query(self, query):
        return [
            {
                "Title": "Title",
                "SubTitle": "SubTitle",
                "IcoPath": "Images/app.png",
                "JSONRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://www.mdcalc.com/"],
                },
            }
        ]

    def context_menu(self, data):
        return [
            {
                "Title": "Title Context",
                "SubTitle": "SubTitle Context",
                "IcoPath": "Images/app.png",
                "JSONRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://www.mdcalc.com/"],
                },
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)


print("I am here to be a breakpoint uwu")
