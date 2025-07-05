import pandas as pd
import datetime as dt
import numpy as np

myline = range(0, 15000)
df = pd.DataFrame({'linear': myline})
df['sines'] = np.sin(df['linear']/6.28)
df['cosines'] = np.cos(df['linear']/6.28)

df['timestamps'] = pd.to_datetime('2025-07-03') + pd.to_timedelta(df['linear'].values, unit='s')

df.set_index('timestamps', inplace=True)

df.to_csv('example_dataframe_time.csv')

print(df)