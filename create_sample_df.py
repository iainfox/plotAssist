import pandas as pd
import numpy as np

n_points = 100
time_seconds = np.linspace(0, 100, n_points)

# Create base signals
df = pd.DataFrame({
    'linear': range(0, n_points),
    'sine': np.sin(2 * np.pi * time_seconds / 20), 
    'cosine': np.cos(2 * np.pi * time_seconds / 20)
})

np.random.seed(42)

df['engine_rpm'] = 2500 + 500 * np.sin(2 * np.pi * time_seconds / 15) + np.random.normal(0, 50, n_points)

df['oil_pressure'] = 45 + 5 * np.sin(2 * np.pi * time_seconds / 25) + np.random.normal(0, 2, n_points)

df['coolant_temp'] = 85 + 10 * (time_seconds / 100) + 3 * np.sin(2 * np.pi * time_seconds / 30) + np.random.normal(0, 1.5, n_points)

df['fuel_flow'] = 12 + 8 * (df['engine_rpm'] - 2500) / 500 + np.random.normal(0, 0.5, n_points)

df['exhaust_temp'] = 400 + 100 * np.roll(df['fuel_flow'] / 20, 5) + np.random.normal(0, 10, n_points)

start_time = pd.to_datetime('2025-07-03 00:00:00')
df['timestamps'] = start_time + pd.to_timedelta(time_seconds, unit='s')

df.set_index('timestamps', inplace=True)

df.to_csv('example_dataframe_time.csv')

print("Dataset created successfully!")
print(f"Shape: {df.shape}")
print(f"Time range: {df.index[0]} to {df.index[-1]}")
print("\nFirst few rows:")
print(df.head())