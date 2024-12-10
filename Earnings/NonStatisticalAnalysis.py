import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from Earnings.AnalysisStats import dataframes
from Earnings.FinancialStats import convert_to_number
import matplotlib.pyplot as plt
import seaborn as sns

# Load the raw data from EarningsReports.py
top_analysts_df = dataframes['top_analysts_df']
revenue_earnings_df = dataframes['revenue_earnings_df']
analyst_price_targets_df = dataframes['analyst_price_targets_df']

# Clean up column names by stripping trailing spaces
top_analysts_df.columns = top_analysts_df.columns.str.strip()

# Check the columns in top_analysts_df
print("Columns in top_analysts_df:", top_analysts_df.columns)

# If 'Date' column is not present, print the first few rows to identify the correct column
if 'Date' not in top_analysts_df.columns:
    print("First few rows of top_analysts_df:")
    print(top_analysts_df.head())

# Assuming the correct column name is 'Date', convert it to datetime
if 'Date' in top_analysts_df.columns:
    top_analysts_df['Date'] = pd.to_datetime(top_analysts_df['Date'])

# Convert relevant columns to numeric, coercing errors to NaN
top_analysts_df['Overall Score'] = pd.to_numeric(top_analysts_df['Overall Score'], errors='coerce')
top_analysts_df['Direction Score'] = pd.to_numeric(top_analysts_df['Direction Score'], errors='coerce')
top_analysts_df['Price Score'] = pd.to_numeric(top_analysts_df['Price Score'], errors='coerce')
top_analysts_df['Price Target'] = pd.to_numeric(top_analysts_df['Price Target'], errors='coerce')

# Group by 'Latest Rating' and calculate the mean
print("\nAverage Scores by Latest Rating:")
print(top_analysts_df.groupby('Latest Rating')[['Overall Score', 'Direction Score', 'Price Score']].mean())

# Time-series analysis to observe changes in analyst sentiment
if 'Date' in top_analysts_df.columns:
    print("\nTime-Series Analysis of Analyst Sentiment:")
    print(top_analysts_df.set_index('Date')[['Overall Score', 'Price Target']].resample('M').mean())

# Dataset 2: Revenue vs. Earnings Data
print("\nRevenue vs. Earnings Data Analysis:")

revenue_earnings_df['Revenue'] = revenue_earnings_df['Revenue'].apply(convert_to_number)
revenue_earnings_df['Earnings'] = revenue_earnings_df['Earnings'].apply(convert_to_number)

# Correlation between Revenue and Earnings
print("\nCorrelation Between Revenue and Earnings:")
print(revenue_earnings_df[['Revenue', 'Earnings']].corr())

# Calculate margins
revenue_earnings_df['Margin'] = revenue_earnings_df['Earnings'] / revenue_earnings_df['Revenue']
print("\nMargins:")
print(revenue_earnings_df[['Quarter', 'Margin']])

# Calculate quarterly growth rates
revenue_earnings_df['Revenue Growth'] = revenue_earnings_df['Revenue'].pct_change()
revenue_earnings_df['Earnings Growth'] = revenue_earnings_df['Earnings'].pct_change()
print("\nQuarterly Growth Rates:")
print(revenue_earnings_df[['Quarter', 'Revenue Growth', 'Earnings Growth']])

# Dataset 3: Analyst Price Targets Data
print("\nAnalyst Price Targets Data Analysis:")

# Convert relevant columns to numeric, coercing errors to NaN
analyst_price_targets_df['Average Price'] = pd.to_numeric(analyst_price_targets_df['Average Price'], errors='coerce')
analyst_price_targets_df['Current Price'] = pd.to_numeric(analyst_price_targets_df['Current Price'], errors='coerce')
top_analysts_df['Price Target'] = pd.to_numeric(top_analysts_df['Price Target'], errors='coerce')

# Calculate the percentage difference
analyst_price_targets_df['Price Gap (%)'] = (analyst_price_targets_df['Average Price'] - analyst_price_targets_df['Current Price']) / analyst_price_targets_df['Current Price'] * 100
print("\nPrice Gap (%):")
print(analyst_price_targets_df[['Current Price', 'Average Price', 'Price Gap (%)']])