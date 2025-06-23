import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

generate = False

if generate:
    some_ints = np.arange(0, 1000)
    df = pd.DataFrame(data=some_ints, columns=['some_ints'])
    df['some_dates'] = pd.to_datetime('2025-06-02') + pd.to_timedelta(df.some_ints/1000, unit='D')

    df.set_index('some_dates', inplace=True)

    df['cosine'] = np.cos(df.some_ints/100 * np.pi)
    df['sine'] = np.sin(df.some_ints/100  * np.pi)
    df['steps'] = (((df.some_ints/10).round(0) % 10)==0).astype(int)
else:
    df = pd.read_csv('example_dataframe.csv')

print("Succsesfully loaded/generated DataFrame")
print(df.head())

fig, axs = plt.subplots(3)
axs[0].plot(df.index, df.cosine, linewidth=0.5)
axs[1].plot(df.index, df.sine, linewidth=0.5)
axs[2].plot(df.index, df.steps, linewidth=0.5)

plt.show()

