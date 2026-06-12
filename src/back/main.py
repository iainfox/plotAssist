import webview
import pandas as pd
import numpy as np

url = "http://localhost:5173"

class Api:
    def __init__(self, channels_dict: dict):
        self._channels_dict = channels_dict

    def get_data(self):
        return self._channels_dict


def start(data: pd.DataFrame):
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
    x = 1000
    cycles = 5
    start_time = "2025-01-01"
    freq = "1min"

    time_index = pd.date_range(
            start=start_time,
            periods=x,
            freq=freq
            )

    t = np.linspace(0, 10, x)

    sine = 5 * (np.sin(2 * np.pi * cycles * t / 10) + 1)
    saw = (t * cycles) % 10

    df = pd.DataFrame(
            {
                "sine": sine,
                "saw": saw,
                },
            index=time_index
            )

    df.index.name = "timestamp"

    start(df)
