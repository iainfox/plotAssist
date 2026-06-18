from dataGen import genData
import webview
from pandas import DataFrame

url = "http://localhost:5173"

class Api:
    def __init__(self, channels_dict: dict):
        self._channels_dict = channels_dict

    def get_data(self):
        return self._channels_dict


def start(data: DataFrame):
    index = data.index.to_numpy().astype(str).tolist()

    channels = []
    for col in data.columns:
        values = data[col].to_numpy()

        channels.append({
            "name": str(col),
            "index": index,
            "datapoints": [float(v) for v in values]
            })

    channels_dict = {"channels": channels}

    api = Api(channels_dict)

    webview.create_window(
            "App",
            url,
            width=1081,
            height=439,
            js_api=api
            )

    webview.start(gui="edgechromium", debug=True)

if __name__ == "__main__":
    df = genData()

    start(df)
