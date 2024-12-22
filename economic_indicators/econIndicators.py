import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
FRED_KEY = os.getenv('FRED_KEY')

def get_fred_data(series_id, api_key, start_date='2023-12-01', end_date='2024-12-31'):
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

def main():
    economic_indicators = get_economic_indicators(FRED_KEY)
    
    with open('economic_indicators/results/economic_indicators.json', 'w') as f:
        json.dump(economic_indicators, f, indent=4)