import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from calculations import calculate_eps_growth, calculate_revenue_growth, calculate_profit_margin, calculate_eps_estimate_spread
from EarningsReports import dataframes

# Load the raw data from EarningsReports.py
top_analysts_df = dataframes['top_analysts_df']
revenue_earnings_df = dataframes['revenue_earnings_df']
analyst_price_targets_df = dataframes['analyst_price_targets_df']

# Example Calculations
def perform_calculations():
    # Example data (replace with actual data from DataFrame)
    current_eps = 2.18
    year_ago_eps = 1.53
    current_revenue = 124.37e9
    year_ago_revenue = 119.58e9
    eps_estimate = 2.35
    revenue_estimate = 124.37e9
    high_estimate = 2.5
    low_estimate = 2.19

    eps_growth = calculate_eps_growth(current_eps, year_ago_eps)
    revenue_growth = calculate_revenue_growth(current_revenue, year_ago_revenue)
    profit_margin = calculate_profit_margin(eps_estimate, revenue_estimate)
    eps_estimate_spread = calculate_eps_estimate_spread(high_estimate, low_estimate)

    print(f"EPS Growth: {eps_growth:.2f}%")
    print(f"Revenue Growth: {revenue_growth:.2f}%")
    print(f"Profit Margin: {profit_margin:.2f}%")
    print(f"EPS Estimate Spread: {eps_estimate_spread:.2f}")

# Perform calculations
perform_calculations()

# Analyze Non-Numeric Data

# Top Analysts Data
def analyze_top_analysts(df):
    # Example: Sentiment Analysis (assuming 'comments' column exists)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['comments'])
    print("Top Analysts Comments Analysis:")
    print(X.toarray())

# Revenue vs. Earnings Data
def analyze_revenue_earnings(df):
    # Example: One-Hot Encoding for categorical features
    encoder = OneHotEncoder()
    X = encoder.fit_transform(df[['category']])
    print("Revenue vs. Earnings Analysis:")
    print(X.toarray())

# Analyst Price Targets Data
def analyze_analyst_price_targets(df):
    # Example: Trend Analysis
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['price_target'].plot(title='Analyst Price Targets Over Time')
    print("Analyst Price Targets Analysis:")
    print(df['price_target'].describe())

# Analyze each non-numeric dataframe
analyze_top_analysts(top_analysts_df)
analyze_revenue_earnings(revenue_earnings_df)
analyze_analyst_price_targets(analyst_price_targets_df)