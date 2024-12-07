from EarningsReports import dataframes

def convert_to_number(value):
    if isinstance(value, str):
        if 'B' in value:
            return float(value.replace('B', '')) * 1e9
        elif 'T' in value:
            return float(value.replace('T', '')) * 1e12
        elif 'M' in value:
            return float(value.replace('M', '')) * 1e6
        elif 'K' in value:
            return float(value.replace('K', '')) * 1e3
        elif '%' in value:
            return float(value.replace('%', '')) / 100
    return float(value)

def calculate_eps_growth(current_eps, year_ago_eps):
    return ((current_eps - year_ago_eps) / year_ago_eps) * 100

def calculate_revenue_growth(current_revenue, year_ago_revenue):
    return ((current_revenue - year_ago_revenue) / year_ago_revenue) * 100

def calculate_profit_margin(eps_estimate, revenue_estimate):
    return (eps_estimate / revenue_estimate) * 100

def calculate_eps_estimate_spread(high_estimate, low_estimate):
    return high_estimate - low_estimate

def calculate_revenue_estimate_spread(high_estimate, low_estimate):
    return high_estimate - low_estimate

def calculate_eps_trend(eps_estimate, eps_7_days_ago, eps_30_days_ago, eps_60_days_ago, eps_90_days_ago):
    trend = {
        'current': eps_estimate,
        '7_days_ago': eps_estimate - eps_7_days_ago,
        '30_days_ago': eps_estimate - eps_30_days_ago,
        '60_days_ago': eps_estimate - eps_60_days_ago,
        '90_days_ago': eps_estimate - eps_90_days_ago
    }
    return trend

def calculate_pe_ratio(stock_price, eps):
    return stock_price / eps

def main():
    # Access the DataFrames from EarningsReports.py
    earnings_df = dataframes['earnings_df']
    revenue_df = dataframes['revenue_df']
    earnings_his = dataframes['earnings_history']
    eps_trend_df = dataframes['eps_trend_df']
    growth_estimate_df = dataframes['growth_estimate_df']
    top_analysts_df = dataframes['top_analysts_df']
    revenue_earnings_df = dataframes['revenue_earnings_df']
    analyst_price_targets_df = dataframes['analyst_price_targets_df']
    
    # Example data (replace with actual data from DataFrame)
    current_eps = float(earnings_his.loc[earnings_his['CURRENCY IN USD'] == 'EPS Actual'].iloc[0, -1])
    year_ago_eps = float(earnings_his.loc[earnings_his['CURRENCY IN USD'] == 'EPS Actual'].iloc[0, -4])
    current_revenue = convert_to_number(revenue_earnings_df.loc[revenue_earnings_df['Quarter'] == 'Quarter 4'].iloc[0, -2])
    year_ago_revenue = convert_to_number(revenue_df.loc[revenue_df['CURRENCY IN USD '] == 'Year Ago Sales'].iloc[0, -4])
    eps_estimate = float(eps_trend_df.loc[eps_trend_df['CURRENCY IN USD '] == 'Current Estimate'].iloc[0, -4])
    revenue_estimate = convert_to_number(revenue_df.loc[revenue_df['CURRENCY IN USD '] == 'Avg. Estimate'].iloc[0, -4])
    eps_high_estimate = float(earnings_df.loc[earnings_df['CURRENCY IN USD '] == 'High Estimate'].iloc[0, -4])
    eps_low_estimate = float(earnings_df.loc[earnings_df['CURRENCY IN USD '] == 'Low Estimate'].iloc[0, -4])
    rev_high_estimate = convert_to_number(revenue_df.loc[revenue_df['CURRENCY IN USD '] == 'High Estimate'].iloc[0, -4])
    rev_low_estimate = convert_to_number(revenue_df.loc[revenue_df['CURRENCY IN USD '] == 'Low Estimate'].iloc[0, -4])
    estimate_7_days_ago = float(eps_trend_df.loc[eps_trend_df['CURRENCY IN USD '] == '7 Days Ago'].iloc[0, -4])
    estimate_30_days_ago = float(eps_trend_df.loc[eps_trend_df['CURRENCY IN USD '] == '30 Days Ago'].iloc[0, -4])
    estimate_60_days_ago = float(eps_trend_df.loc[eps_trend_df['CURRENCY IN USD '] == '60 Days Ago'].iloc[0, -4])
    estimate_90_days_ago = float(eps_trend_df.loc[eps_trend_df['CURRENCY IN USD '] == '90 Days Ago'].iloc[0, -4])
    stock_price = float(analyst_price_targets_df.loc[0, 'Current Price'])

    # Perform calculations
    eps_growth = calculate_eps_growth(current_eps, year_ago_eps)
    revenue_growth = calculate_revenue_growth(current_revenue, year_ago_revenue)
    profit_margin = calculate_profit_margin(eps_estimate, revenue_estimate)
    eps_estimate_spread = calculate_eps_estimate_spread(eps_high_estimate, eps_low_estimate)
    revenue_estimate_spread = calculate_revenue_estimate_spread(rev_high_estimate, rev_low_estimate)
    eps_trend = calculate_eps_trend(eps_estimate, estimate_7_days_ago, estimate_30_days_ago, estimate_60_days_ago, estimate_90_days_ago)
    pe_ratio = calculate_pe_ratio(stock_price, current_eps)
    return {
        'eps_growth': eps_growth,
        'revenue_growth': revenue_growth,
        'profit_margin': profit_margin,
        'eps_estimate_spread': eps_estimate_spread,
        'revenue_estimate_spread': revenue_estimate_spread,
        'eps_trend': eps_trend,
        'pe_ratio': pe_ratio
    }

if __name__ == '__main__':
    main()