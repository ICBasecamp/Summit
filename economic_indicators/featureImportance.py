import pandas as pd
import numpy as np
import json
import os
import sys
from econIndicators import get_economic_indicators

# Add the parent directory to the Python path to import Earnings module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Earnings.AnalysisStats import main as calculate_stats
from utilities import convert_to_number

dataframes = calculate_stats()

def calculate_feature_importance():
    # with open('economic_indicators/results/economic_indicators.json', 'r') as f:
    #     economic_indicators = json.load(f)
    economic_indicators = get_economic_indicators()

    # Convert economic indicators to DataFrame
    econ_df = pd.DataFrame()
    for indicator, data in economic_indicators.items():
        series = pd.Series({item['date']: float(item['value']) for item in data if item['value'] != '.'})
        econ_df[indicator] = series

    # Ensure all dates are included and fill missing values with NaN
    econ_df.index = pd.to_datetime(econ_df.index)
    econ_df = econ_df.sort_index()

    # Manually aggregate economic indicators to quarterly data
    quarterly_econ_df = pd.DataFrame()
    for indicator in econ_df.columns:
        quarterly_values = []
        for i in range(0, len(econ_df), 3):
            quarter_data = econ_df[indicator].iloc[i:i+3]
            quarterly_average = quarter_data.mean()
            quarterly_values.append(quarterly_average)
        quarterly_econ_df[indicator] = quarterly_values

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
        (earnings_df, 'Earnings Reports'),
        (revenue_df, 'Stock Revenue'),
        (earnings_history_df, 'Earnings History'),
        (eps_trend_df, 'EPS Trend')
    ]

    # Initialize dictionary to store average correlations
    average_correlations = {}

    # Perform correlation analysis and feature importance analysis
    for df, name in dataframes_list:
        df = df.transpose()
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])
        df.columns = df.columns.astype(str)

        # Convert relevant columns to numeric using convert_to_number
        for col in df.columns:
            df[col] = df[col].apply(lambda x: convert_to_number(x) if isinstance(x, str) else x)

        # Perform correlation analysis for each target variable in the earnings DataFrame
        overall_correlations = {}
        for target_variable in df.columns:
            if target_variable != 'date':
                correlations = {}
                for econ_indicator in quarterly_econ_df.columns:
                    # Ensure that the data is being pulled correctly
                    target_data = df[target_variable].dropna().values
                    econ_data = quarterly_econ_df[econ_indicator].dropna().values

                    # Calculate the correlation coefficient
                    if len(target_data) > 0 and len(econ_data) > 0:
                        correlation = np.corrcoef(target_data, econ_data)[0, 1]
                        correlations[econ_indicator] = correlation
                    else:
                        correlations[econ_indicator] = np.nan

                # Aggregate correlations for overall analysis
                for econ_indicator, correlation in correlations.items():
                    if econ_indicator not in overall_correlations:
                        overall_correlations[econ_indicator] = []
                    overall_correlations[econ_indicator].append(correlation)

        # Calculate average correlation for each economic indicator
        avg_correlations = {econ_indicator: np.nanmean(correlations) for econ_indicator, correlations in overall_correlations.items()}
        avg_correlation_df = pd.DataFrame(list(avg_correlations.items()), columns=['Economic Indicator', 'Average Correlation'])
        avg_correlation_df = avg_correlation_df.sort_values(by='Average Correlation', ascending=False)
        average_correlations[name] = avg_correlations
        
    return average_correlations    
