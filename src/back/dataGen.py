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
    cosine = 5 * (np.cos(2 * np.pi * cycles * t / 10) + 1)
    saw = (t * cycles) % 10
    square = 10 * (np.sin(2 * np.pi * cycles * t / 10) > 0).astype(float)

    quadratic = (t - 5) ** 2
    cubic = (t - 5) ** 3
    exp_growth = np.exp(0.3 * (t - 5))
    log_curve = np.log1p(t)

    tanh = np.tanh(t - 5)
    sigmoid = 1 / (1 + np.exp(-(t - 5)))

    noise = np.random.normal(0, 0.5, x)
    random_walk = np.cumsum(np.random.normal(0, 0.2, x))

    amplitude_modulated = sine * (1 + 0.5 * np.sin(2 * np.pi * t))
    mixed = sine * cosine

    sine_diff = np.gradient(sine)
    saw_diff = np.gradient(saw)

    df = pd.DataFrame(
        {
            "sine": sine,
            "cosine": cosine,
            "saw": saw,
            "square": square,

            "quadratic": quadratic,
            "cubic": cubic,
            "exp_growth": exp_growth,
            "log_curve": log_curve,

            "tanh": tanh,
            "sigmoid": sigmoid,

            "noise": noise,
            "random_walk": random_walk,

            "amplitude_modulated": amplitude_modulated,
            "mixed": mixed,

            "sine_diff": sine_diff,
            "saw_diff": saw_diff,
        },
        index=time_index
    )

    df.index.name = "timestamp"

    return df

if __name__ == "__main__":
    data = genData()
    data.to_json("./data/data.json")