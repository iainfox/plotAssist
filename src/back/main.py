import webview
from pathlib import Path

DEV = True

if DEV:
    url = "http://localhost:5173"
else: 
    frontend = (
            Path(__file__).resolve().parent.parent
            / "front"
            / "dist"
            / "index.html"
            )

    if not frontend.exists():
        raise FileNotFoundError(f"frontend build not found: {frontend}")

    url = frontend.as_uri()

webview.create_window("App", url, width=1081, height=439)
webview.start(gui='edgechromium', debug=True)
