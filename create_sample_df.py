import pandas as pd
import numpy as np

n_points = 100
time_seconds = np.linspace(0, 100, n_points)

df = pd.DataFrame({
    'linear': range(0, n_points),
    'sine': np.sin(2 * np.pi * time_seconds / 20), 
    'cosine': np.cos(2 * np.pi * time_seconds / 20)
})

start_time = pd.to_datetime('2025-07-03 00:00:00')
df['timestamps'] = start_time + pd.to_timedelta(time_seconds, unit='s')

df.set_index('timestamps', inplace=True)

df.to_csv('example_dataframe_time.csv')

print("Dataset created successfully!")
print(f"Shape: {df.shape}")
print(f"Time range: {df.index[0]} to {df.index[-1]}")
print("\nFirst few rows:")
print(df.head())