import pandas as pd
import numpy as np

def genData():
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

    return df

if __name__ == "__main__":
    data = genData()
    data.to_json("./data/data.json")