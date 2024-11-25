import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
FRED_KEY = os.getenv('FRED_KEY')  # FRED API Key

def get_fred_data(series_id, api_key):
    current_date = datetime.now()
    previous_year_date = current_date.replace(year=current_date.year - 1)
    start_date = previous_year_date.strftime('%Y-%m-%d')
    end_date = current_date.strftime('%Y-%m-%d')
    
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}'
    response = requests.get(url)
    data = response.json()
    
    if 'observations' in data:
        return data['observations']
    else:
        print(f"Error fetching data for series_id {series_id}: {data}")
        return []

def get_economic_indicators(api_key):
    indicators = {
        'Treasury Yield': 'DGS10',  # 10-Year Treasury Constant Maturity Rate
        'FED Rate': 'FEDFUNDS',  # Effective Federal Funds Rate
        'CPI': 'CPIAUCSL',  # Consumer Price Index for All Urban Consumers: All Items
        'Retail Sales': 'RSAFS',  # Retail Sales: Retail Trade
        'Durable Goods Orders': 'DGORDER',  # Manufacturers' New Orders: Durable Goods
        'Unemployment Rate': 'UNRATE',  # Unemployment Rate
        'Nonfarm Payroll': 'PAYEMS'  # All Employees, Total Nonfarm
    }

    results = {}
    for indicator, series_id in indicators.items():
        data = get_fred_data(series_id, api_key)
        results[indicator] = data

    return results

if __name__ == '__main__':
    economic_indicators = get_economic_indicators(FRED_KEY)
    
    for indicator, data in economic_indicators.items():
        print(f"\n{indicator}:")
        for entry in data:
            print(f"{entry['date']}: {entry['value']}")