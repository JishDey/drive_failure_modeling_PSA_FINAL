#!/Users/thundergod/workspace/EE24/final_project/.venv/bin/python3
import pandas as pd
import sys
import os

# This file(will) automatically compile files into the drive survival data.
# You can check the data by running the file interactively and calling `check`

# the data directory, containing csv files
# this block could be improved by os.walk, but this is good enough for now 
def quarter_stack(quarter_dir: str, data_dir: str = 'data'):
        dfs = []
        for i, file in enumerate(os.listdir(data_dir + "/" + quarter_dir)):
                df = pd.read_csv(f'{data_dir}/{quarter_dir}/{file}', 
                                usecols=['date', 'serial_number', 'model', 'failure', 'smart_9_raw'])
                df['date'] = pd.to_datetime(df['date'])
                df['serial_number'] = df['serial_number'].astype('category')
                df['model'] = df['model'].astype('category')
                dfs.append(df)
                print(f"quarter: {quarter_dir},file number {i}")

        # stacking the dataframes into one - like an 'append'
        stacked_df = pd.concat(dfs)

        # grouping the data so that each drive (marked by serial) is one
        # this is similar to a 'join over index'
        grouped = stacked_df.groupby('serial_number').agg(
			first_date=('date', 'min'),
			last_date=('date', 'max'),
			failed=('failure', 'max'),
			model=('model', 'first'),
			smart9=('smart_9_raw', 'max')
		).reset_index()

        # output to file
        grouped.to_csv(f"merged_quarters/{quarter_dir}_data.csv", index=False) 

def check(lifetime_df):
    print(lifetime_df.head())
    print(lifetime_df['failed'].value_counts())
    print(lifetime_df['lifetime_days'].describe())

if __name__ == "__main__":
    if len(sys.argv) == 2:
        quarter_dir = sys.argv[1]
        quarter_stack(quarter_dir)
    elif len(sys.argv) == 3 and sys.argv[1] == '--check':
        quarter_dir = sys.argv[2]
        lifetime_df = pd.read_csv(f"{quarter_dir}_data.csv")
        check(lifetime_df)
    else:
        print("Usage: python stack_tables.py <quarter_dir>")
        sys.exit(1)
