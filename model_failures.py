#!/Users/thundergod/workspace/EE24/final_project/.venv/bin/python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

# load processed dataset (TODO: to be extended to multiple datasets)
df = pd.read_csv('lifetime_data.csv')
df.dropna(subset=['smart9'], inplace=True)

# TODO: possible move to a third 'tools' file after figuring out in-project 
# imports
def check():
    print(df.head())
    print(df['failed'].value_counts())
    print(df['smart9'].describe())

failed_df = df[df['failed'] == 1].copy()
bins = np.linspace(failed_df['smart9'].min(), 
                   failed_df['smart9'].max(), 
                   15)
failed_df['age_bin'] = pd.cut(failed_df['smart9'], bins=bins)
bin_counts = failed_df['age_bin'].value_counts().sort_index()
bin_counts.plot(kind='bar')
plt.xlabel('Age bin (SMART 9)')
plt.ylabel('Number of failures')
plt.title('Failures by Age Bin')
plt.xticks(rotation=45)
plt.show()

def check_failed():
    print("Number of failed drives:", len(failed_df))
    print(failed_df['smart9'].describe())

def estimate_exponential():
    T = failed_df['smart9'].values

    mean_T = np.mean(T)
    var_T = np.var(T, ddof=1)
    skew_T = skew(T)
    kurt_T = kurtosis(T)

    lambda_hat = 1 / mean_T

    print(f"Empirical Mean: {mean_T:.4f}")
    print(f"Empirical Variance: {var_T:.4f}")
    print(f"Estimated lambda (MLE): {lambda_hat:.6f}")

    return lambda_hat, mean_T, var_T, skew_T, kurt_T

def compare_stats(lambda_hat, empirical_mean, empirical_var, empirical_skew, 
                                                        empirical_kurt):
    theoretical_mean = 1 / lambda_hat
    theoretical_var = (1 - lambda_hat) / (lambda_hat ** 2)
    theoretical_skew = (2 - lambda_hat) / np.sqrt(1 - lambda_hat)
    theoretical_kurt = 6 + (lambda_hat ** 2) / (1 - lambda_hat)


    print("\n--- Comparison ---")
    print(f"Theoretical Mean: {theoretical_mean:.4f}")
    print(f"Empirical Mean:   {empirical_mean:.4f}")
    print("         - - -")
    print(f"Theoretical Var:  {theoretical_var:.4f}")
    print(f"Empirical Var:    {empirical_var:.4f}")
    print("         - - -")
    print(f"Theoretical Skew: {theoretical_skew:.4f}")
    print(f"Empirical Skew:   {empirical_skew:.4f}")
    print("         - - -")
    print(f"Theoretical Kurt: {theoretical_kurt:.4f}")
    print(f"Empirical Kurt:   {empirical_kurt:.4f}")

def simulate_exponential(lambda_hat, N=10000):
    simulated = np.random.exponential(1 / lambda_hat, size=N)
    return simulated

def plot_comparison(real_data, simulated_data):
    plt.hist(real_data, bins=30, alpha=0.5, label='Real Data', density=True)
    plt.hist(simulated_data, bins=30, alpha=0.5, label='Exponential Sim', density=True)
    
    plt.xlabel('Lifetime (hours)')
    plt.ylabel('Density')
    plt.title('Real vs Exponential Distribution')
    plt.legend()
    plt.show()
    

def main():
    check_failed()
    lambda_hat, mean_T, var_T, skew_T, kurt_T = estimate_exponential()
    compare_stats(lambda_hat, mean_T, var_T, skew_T, kurt_T)
    simulated = simulate_exponential(lambda_hat, N=len(failed_df))
    plot_comparison(failed_df['smart9'], simulated)


if __name__ == "__main__":
    main()