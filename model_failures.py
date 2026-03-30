import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load processed dataset (TODO: to be extended to multiple datasets)
df = pd.read_csv('lifetime_data.csv')

def check():
    print(df.head())
    print(df['failed'].value_counts())
    print(df['lifetime_days'].describe())