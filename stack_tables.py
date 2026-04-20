import pandas as pd
import os

# This file(will) automatically compile files into the drive survival data.
# You can check the data by running the file interactively and calling `check`

# the data directory, containing csv files
# this block could be improved by os.walk, but this is good enough for now 
data_dir = 'merged_quarters'
data_subdirs = os.listdir(data_dir)
dfs = []
for i, file in enumerate(os.listdir(data_dir)):
        df = pd.read_csv(f'{data_dir}/{file}', 
                         parse_dates=['first_date', 'last_date'])
        df['serial_number'] = df['serial_number'].astype('category')
        df['model'] = df['model'].astype('category')
        dfs.append(df)
        print(f"{i}: {file}")

# stacking the dataframes into one - like an 'append'
stacked_df = pd.concat(dfs)

# grouping the data so that each drive (marked by serial) is one
# this is similar to a 'join over index'
grouped = stacked_df.groupby('serial_number')
lifetime_df = grouped.agg({
    'first_date': 'min',
    'last_date': 'max',
    'failed': 'max',
    'model': 'first',
    'smart9': 'max'
})

lifetime_df.columns = ['first_date', 'last_date', 'failed', 'model', 'smart9']

# find the lifetime of each drive in days, by subtracting the first date from the last date
lifetime_df['lifetime_days'] = (
    lifetime_df['last_date'] - lifetime_df['first_date']
).dt.days + 1

lifetime_df = lifetime_df.reset_index()

# should be labeled per-quarter eventually
lifetime_df.to_csv('lifetime_data.csv', index=False) 

def check():
    print(lifetime_df.head())
    print(lifetime_df['failed'].value_counts())
    print(lifetime_df['lifetime_days'].describe())

