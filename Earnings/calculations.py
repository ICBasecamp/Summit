import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio
from EarningsReports import ticker
from datetime import datetime

url_statistics = f'https://finance.yahoo.com/quote/{ticker}/key-statistics/'
url_quote = f'https://finance.yahoo.com/quote/{ticker}/'

async def fetch_financial_metrics(page):
    await page.wait_for_selector('section[data-testid="qsp-statistics"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    metrics = {}

    # Valuation Measures
    valuation_section = soup.find('section', {'data-testid': 'qsp-statistics'})
    if valuation_section:
        print("Found Valuation Measures section")
        valuation_table = valuation_section.find('table')
        if valuation_table:
            for row in valuation_table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) > 1:
                    label = cells[0].text.strip()
                    current_value = cells[1].text.strip()  # Get the current value
                    if any(key in label for key in ['Forward P/E', 'PEG Ratio', 'Price/Sales', 'Enterprise Value/EBITDA']):
                        metrics[label] = current_value

    # Profitability Metrics
    sections = soup.find_all('section', class_='card small tw-p-0 yf-1yegwxr sticky noBackGround')
    for section in sections:
        header = section.find('h3', string='Profitability')
        if header:
            print("Found Profitability section")
            table = header.find_next('table')
            if table:
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) > 1:
                        label = cells[0].text.strip()
                        value = cells[1].text.strip()
                        if any(key in label for key in ['Profit Margin', 'Operating Margin']):
                            print(f"{label}: {value}")
                            metrics[label] = value
            break

    # Management Effectiveness
    for section in sections:
        header = section.find('h3', string='Management Effectiveness')
        if header:
            print("Found Management Effectiveness section")
            table = header.find_next('table')
            if table:
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) > 1:
                        label = cells[0].text.strip()
                        value = cells[1].text.strip()
                        if any(key in label for key in ['Return on Assets', 'Return on Equity']):
                            print(f"{label}: {value}")
                            metrics[label] = value
            break

    # Growth Metrics
    for section in sections:
        header = section.find('h3', string='Growth Metrics')
        if header:
            print("Found Growth Metrics section")
            table = header.find_next('table')
            if table:
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) > 1:
                        label = cells[0].text.strip()
                        value = cells[1].text.strip()
                        if any(key in label for key in ['Quarterly Revenue Growth', 'Quarterly Earnings Growth', 'Diluted EPS']):
                            print(f"{label}: {value}")
                            metrics[label] = value
            break

    print(metrics)
    return metrics

async def fetch_quote_metrics(page):
    await page.wait_for_selector('div[data-testid="quote-statistics"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    metrics = {}

    # Quote Metrics
    quote_section = soup.find('div', {'data-testid': 'quote-statistics'})
    if quote_section:
        print("Found Quote Statistics section")
        items = quote_section.find_all('li')
        for item in items:
            label = item.find('span', class_='label').text.strip()
            value = item.find('span', class_='value').text.strip()
            if any(key in label for key in ['PE Ratio (TTM)', 'EPS (TTM)', 'Earnings Date']):
                metrics[label] = value

    # Calculate days till earnings
    if 'Earnings Date' in metrics:
        earnings_date_str = metrics['Earnings Date']
        earnings_date = datetime.strptime(earnings_date_str, '%b %d, %Y')
        today = datetime.today()
        days_till_earnings = (earnings_date - today).days
        metrics['Days till Earnings'] = days_till_earnings

    return metrics

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url_statistics)
        financial_metrics = await fetch_financial_metrics(page)
        
        await page.goto(url_quote)
        quote_metrics = await fetch_quote_metrics(page)
        
        # Combine both metrics
        all_metrics = {**financial_metrics, **quote_metrics}
        
        # Return the combined metrics
        return all_metrics

# Run the main function and get the financial metrics
all_metrics = asyncio.run(main())
print(all_metrics)