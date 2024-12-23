import pandas as pd
from earnings.AnalysisStats import main as calculate_stats
from utilities import convert_to_number

async def main(ticker):
    dataframes = await calculate_stats(ticker)
    
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
    average_scores_by_rating = top_analysts_df.groupby('Latest Rating')[['Overall Score', 'Direction Score', 'Price Score']].mean()

    # Time-series analysis to observe changes in analyst sentiment
    time_series_analysis = None
    if 'Date' in top_analysts_df.columns:
        time_series_analysis = top_analysts_df.set_index('Date')[['Overall Score', 'Price Target']].resample('M').mean()

    # Dataset 2: Revenue vs. Earnings Data
    revenue_earnings_df['Revenue'] = revenue_earnings_df['Revenue'].apply(convert_to_number)
    revenue_earnings_df['Earnings'] = revenue_earnings_df['Earnings'].apply(convert_to_number)

    # Correlation between Revenue and Earnings
    correlation = revenue_earnings_df[['Revenue', 'Earnings']].corr()

    # Calculate margins
    revenue_earnings_df['Margin'] = revenue_earnings_df['Earnings'] / revenue_earnings_df['Revenue']
    margins = revenue_earnings_df[['Quarter', 'Margin']]

    # Calculate quarterly growth rates
    revenue_earnings_df['Revenue Growth'] = revenue_earnings_df['Revenue'].pct_change()
    revenue_earnings_df['Earnings Growth'] = revenue_earnings_df['Earnings'].pct_change()
    quarterly_growth_rates = revenue_earnings_df[['Quarter', 'Revenue Growth', 'Earnings Growth']]

    # Dataset 3: Analyst Price Targets Data
    analyst_price_targets_df['Average Price'] = pd.to_numeric(analyst_price_targets_df['Average Price'], errors='coerce')
    analyst_price_targets_df['Current Price'] = pd.to_numeric(analyst_price_targets_df['Current Price'], errors='coerce')
    analyst_price_targets_df['Price Gap (%)'] = (analyst_price_targets_df['Average Price'] - analyst_price_targets_df['Current Price']) / analyst_price_targets_df['Current Price'] * 100
    price_gap = analyst_price_targets_df[['Current Price', 'Average Price', 'Price Gap (%)']]

    # Convert Timestamp keys to strings
    if time_series_analysis is not None:
        time_series_analysis.index = time_series_analysis.index.astype(str)

    # Save the results to a dictionary
    non_statistical_results = {
        'average_scores_by_rating': average_scores_by_rating.to_dict(),
        'time_series_analysis': time_series_analysis.to_dict() if time_series_analysis is not None else None,
        'correlation': correlation.to_dict(),
        'margins': margins.to_dict(),
        'quarterly_growth_rates': quarterly_growth_rates.to_dict(),
        'price_gap': price_gap.to_dict()
    }

    return non_statistical_results