import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

# load processed dataset (TODO: to be extended to multiple datasets)
df = pd.read_csv('lifetime_data.csv')

# TODO: possible move to a third 'tools' file after figuring out in-project 
# imports
def check():
    print(df.head())
    print(df['failed'].value_counts())
    print(df['lifetime_days'].describe())

failed_df = df[df['failed'] == 1].copy()

def check_failed():
    print("Number of failed drives:", len(failed_df))
    print(failed_df['lifetime_days'].describe())

def estimate_geometric():
    T = failed_df['lifetime_days'].values

    mean_T = np.mean(T)
    var_T = np.var(T, ddof=1)
    skew_T = skew(T)
    kurt_T = kurtosis(T)

    p_hat = 1 / mean_T

    print(f"Empirical Mean: {mean_T:.4f}")
    print(f"Empirical Variance: {var_T:.4f}")
    print(f"Estimated p (MLE): {p_hat:.6f}")

    return p_hat, mean_T, var_T, skew_T, kurt_T

def compare_stats(p_hat, empirical_mean, empirical_var, empirical_skew, 
                                                        empirical_kurt):
    theoretical_mean = 1 / p_hat
    theoretical_var = (1 - p_hat) / (p_hat ** 2)
    theoretical_skew = (2 - p_hat) / np.sqrt(1 - p_hat)
    theoretical_kurt = 6 + (p_hat ** 2) / (1 - p_hat)


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

def simulate_geometric(p_hat, N=10000):
    simulated = np.random.geometric(p_hat, size=N)
    return simulated

def plot_comparison(real_data, simulated_data):
    plt.hist(real_data, bins=30, alpha=0.5, label='Real Data', density=True)
    plt.hist(simulated_data, bins=30, alpha=0.5, label='Geometric Sim', density=True)
    
    plt.xlabel('Lifetime (days)')
    plt.ylabel('Density')
    plt.title('Real vs Geometric Distribution')
    plt.legend()
    plt.show()
    

def main():
    check_failed()
    p_hat, mean_T, var_T, skew_T, kurt_T = estimate_geometric()
    compare_stats(p_hat, mean_T, var_T, skew_T, kurt_T)
    simulated = simulate_geometric(p_hat, N=len(failed_df))
    plot_comparison(failed_df['lifetime_days'], simulated)


if __name__ == "__main__":
    main()