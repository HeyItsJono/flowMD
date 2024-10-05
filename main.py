import sys
from pathlib import Path

# Bootstrap code for the FlowLauncher plugin to allow for importing of external modules. Needs to be placed before said exteral modules (webbrowser, flowlauncher, calcs) are imported. Calcs is a local file, but contains its own external modules (bs4, requests).
plugindir = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "flowmd")
sys.path = [str(plugindir / p) for p in paths] + sys.path

from flowmd import flowMD  # noqa: E402

if __name__ == "__main__":
    flowMD.run()
