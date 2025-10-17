import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResultsWrapper
from typing import Tuple

BENCHMARK_START = '2022-01'
BENCHMARK_END = '2023-12'

EVENT_START = '2024-01'
EVENT_END = '2024-06' 

def load_and_prepare_data() -> pd.DataFrame:
    try:
        df_pi = pd.read_csv('Sentiment Index.csv', header=1)
        df_pi['Month'] = pd.to_datetime(df_pi['Month'], format='%Y-%m')
        df_pi.set_index('Month', inplace=True)
        print("PI data loaded successfully.")
    except FileNotFoundError:
        print("Error: 'Sentiment Index.csv' not found.")
        return pd.DataFrame()

    try:
        df_market = pd.read_csv('NHPI_and_Sales_Growth.csv', header=1)
        df_market['Month'] = pd.to_datetime(df_market['Month'], format='%Y-%m')
        df_market.set_index('Month', inplace=True)
        print("Market data loaded successfully.")
    except FileNotFoundError:
        print("Error: 'NHPI_and_Sales_Growth.csv' not found.")
        return pd.DataFrame()

    df_combined = df_pi.merge(df_market, left_index=True, right_index=True, how='inner')
    df_combined = df_combined.sort_index()

    df_combined['PI_L1'] = df_combined['PI'].shift(1)       # PI(t-1)
    df_combined['NHPI_L1'] = df_combined['NHPI'].shift(1)   # NHPI(t-1)
    df_combined['NHPI_L2'] = df_combined['NHPI'].shift(2)   # NHPI(t-2)

    df_combined = df_combined.dropna(subset=['PI_L1', 'NHPI_L1', 'NHPI_L2'])
    
    print(f"\nCombined Data Shape: {df_combined.shape}")
    print(f"Combined Data Head (after lags): \n{df_combined.head()}")
    
    return df_combined

def fit_benchmark_model(df_data: pd.DataFrame) -> Tuple[RegressionResultsWrapper, pd.DataFrame]:
    df_benchmark = df_data.loc[BENCHMARK_START:BENCHMARK_END]
    Y = df_benchmark['PI']
    X = df_benchmark[['PI_L1', 'NHPI_L1', 'NHPI_L2']]
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    
    print("\n--- Benchmark Model Fit Results (OLS) ---")
    print(results.summary())
    
    return results, df_data

def calculate_abnormal_returns(results: RegressionResultsWrapper, df_data: pd.DataFrame) -> pd.DataFrame:
    df_event = df_data.loc[EVENT_START:EVENT_END].copy()
    X_event = df_event[['PI_L1', 'NHPI_L1', 'NHPI_L2']]
    X_event = sm.add_constant(X_event, has_constant='add')
    df_event['NR'] = results.predict(X_event)
    df_event['AR'] = df_event['PI'] - df_event['NR']
    car = df_event['AR'].sum()
    
    print("\n--- Event Study Results ---")
    print("Abnormal Returns (AR) and Cumulative Abnormal Returns (CAR) for Event Window:")
    print(df_event[['PI', 'NR', 'AR']])
    print(f"\nCalculated Cumulative Abnormal Returns (CAR) for {EVENT_START} to {EVENT_END}: {car:.4f}")
    reported_car = 0.2509
    if np.isclose(car, reported_car, atol=0.001):
        print("\nVerification: Calculated CAR matches the reported value (0.2509) closely.")
    else:
        print(f"\nVerification: Calculated CAR ({car:.4f}) does NOT match the reported value (0.2509).")
        print("This discrepancy may be due to differences in data trimming or calculation methods in EViews.")
        
    return df_event

if __name__ == '__main__':
    df = load_and_prepare_data()
    if df.empty:
        exit()
    results, df_full = fit_benchmark_model(df)
    df_results = calculate_abnormal_returns(results, df_full)
