from EarningsReports import dataframes

def convert_to_number(value):
    if 'B' in value:
        return float(value.replace('B', '')) * 1e9
    elif 'T' in value:
        return float(value.replace('T', '')) * 1e12
    elif 'M' in value:
        return float(value.replace('M', '')) * 1e6
    elif 'K' in value:
        return float(value.replace('K', '')) * 1e3
    else:
        return float(value)

def calculate_eps_growth(current_eps, year_ago_eps):
    return ((current_eps - year_ago_eps) / year_ago_eps) * 100

def calculate_revenue_growth(current_revenue, year_ago_revenue):
    return ((current_revenue - year_ago_revenue) / year_ago_revenue) * 100

def calculate_profit_margin(eps_estimate, revenue_estimate):
    return (eps_estimate / revenue_estimate) * 100

def calculate_estimate_spread(high_estimate, low_estimate):
    return high_estimate - low_estimate

def calculate_revision_trend(current_estimate, estimate_30_days_ago):
    return current_estimate - estimate_30_days_ago

def calculate_pe_ratio(stock_price, eps):
    return stock_price / eps

def calculate_ps_ratio(stock_price, revenue_per_share):
    return stock_price / revenue_per_share

def calculate_revenue_per_employee(total_revenue, number_of_employees):
    return total_revenue / number_of_employees

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
    
    print("Columns in earnings_df:", revenue_df.columns)
    
    # Example data (replace with actual data from DataFrame)
    current_eps = float(earnings_his.loc[earnings_his['CURRENCY IN USD'] == 'EPS Actual'].iloc[0, -1])
    print(current_eps)
    year_ago_eps = float(earnings_his.loc[earnings_his['CURRENCY IN USD'] == 'EPS Actual'].iloc[0, -4])
    print(year_ago_eps)
    current_revenue = convert_to_number(revenue_df.loc[revenue_df['CURRENCY IN USD '] == 'Avg. Estimate'].iloc[0, -4])
    print(current_revenue)
    year_ago_revenue = convert_to_number(revenue_df.loc[revenue_df['CURRENCY IN USD '] == 'Year Ago Sales'].iloc[0, -4])
    print(year_ago_revenue)
    eps_estimate = 2.40
    revenue_estimate = 105000000
    high_estimate = 2.50
    low_estimate = 2.20
    current_estimate = 2.45
    estimate_30_days_ago = 2.30
    stock_price = 300
    revenue_per_share = 50
    total_revenue = 1000000000
    number_of_employees = 10000
    
    # Perform calculations
    eps_growth = calculate_eps_growth(current_eps, year_ago_eps)
    revenue_growth = calculate_revenue_growth(current_revenue, year_ago_revenue)
    profit_margin = calculate_profit_margin(eps_estimate, revenue_estimate)
    estimate_spread = calculate_estimate_spread(high_estimate, low_estimate)
    revision_trend = calculate_revision_trend(current_estimate, estimate_30_days_ago)
    pe_ratio = calculate_pe_ratio(stock_price, current_eps)
    ps_ratio = calculate_ps_ratio(stock_price, revenue_per_share)
    revenue_per_employee = calculate_revenue_per_employee(total_revenue, number_of_employees)
    
    # Print results
    print(f"EPS Growth: {eps_growth}%")
    print(f"Revenue Growth: {revenue_growth}%")
    print(f"Profit Margin: {profit_margin}%")
    print(f"Estimate Spread: {estimate_spread}")
    print(f"Revision Trend: {revision_trend}")
    print(f"P/E Ratio: {pe_ratio}")
    print(f"P/S Ratio: {ps_ratio}")
    print(f"Revenue per Employee: {revenue_per_employee}")

if __name__ == '__main__':
    main()