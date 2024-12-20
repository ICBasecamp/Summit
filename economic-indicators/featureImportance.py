import pandas as pd
import numpy as np
import json
import os
import sys

# Add the parent directory to the Python path to import Earnings module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Earnings.AnalysisStats import dataframes
from utilities import convert_to_number, random_forest_feature_importance

# Load economic indicators data
with open('economic_indicators.json', 'r') as f:
    economic_indicators = json.load(f)

# Convert economic indicators to DataFrame
econ_df = pd.DataFrame()
for indicator, data in economic_indicators.items():
    series = pd.Series({item['date']: float(item['value']) for item in data if item['value'] != '.'})
    econ_df[indicator] = series

# Ensure all dates are included and fill missing values with NaN
econ_df.index = pd.to_datetime(econ_df.index)
econ_df = econ_df.sort_index()

# Load the raw data from EarningsReports.py
earnings_df = dataframes['earnings_df']
revenue_df = dataframes['revenue_df']
earnings_history_df = dataframes['earnings_history']
eps_trend_df = dataframes['eps_trend_df']

# Drop rows with all NaN values
earnings_history_df = earnings_history_df.dropna(how='all')

# Reset indices to ensure proper stacking
earnings_df = earnings_df.reset_index(drop=True)
revenue_df = revenue_df.reset_index(drop=True)
earnings_history_df = earnings_history_df.reset_index(drop=True)
eps_trend_df = eps_trend_df.reset_index(drop=True)

# List of dataframes
dataframes_list = [
    (earnings_df, 'earnings_df'),
    (revenue_df, 'revenue_df'),
    (earnings_history_df, 'earnings_history_df'),
    (eps_trend_df, 'eps_trend_df')
]

# Perform correlation analysis and feature importance analysis
for df, name in dataframes_list:
    
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])

    # Convert all column names to strings
    df.columns = df.columns.astype(str)

    # Convert relevant columns to numeric using convert_to_number
    for col in df.columns:
        df[col] = df[col].apply(lambda x: convert_to_number(x) if isinstance(x, str) else x)

    # Perform correlation analysis for each target variable in the earnings DataFrame
    for target_variable in df.columns:
        if target_variable != 'date':

            X = econ_df.columns
            Y = target_variable

            # Perform feature importance analysis using the function from utilities.py
            feature_importances = random_forest_feature_importance(X, Y)
            if feature_importances.empty:
                print(f"No feature importances found for {target_variable} in {name}.")
                continue

            # Output feature importances
            print(f"Feature Importances for {target_variable} in {name}:")
            print(feature_importances)