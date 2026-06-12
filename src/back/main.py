import webview
import pandas as pd

DEV = True

url = "http://localhost:5173"

class Api:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def get_data(self):
        data = self.data.to_json()
        if (not data):
            raise Exception("Couldn't convert data to json")

        return data

def start(data: pd.DataFrame):
    api = Api(data)

    webview.create_window("App", url, width=1081, height=439, js_api=api)
    webview.start(gui='edgechromium', debug=True)
