import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio

async def fetch_earnings_estimate(page):
    await page.wait_for_selector('section[data-testid="earningsEstimate"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    earnings_section = soup.find('section', {'data-testid': 'earningsEstimate'})
    
    if earnings_section:
        print("Found Earnings Estimate section")
        
        # Extract table data
        table = earnings_section.find('table')
        if table:
            headers = [th.text for th in table.find_all('th')]
            
            data_rows = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                data = [col.text for col in columns]
                data_rows.append(data)
            
            # Create a DataFrame
            df = pd.DataFrame(data_rows[1:], columns=headers)
            return df
    return pd.DataFrame()

async def fetch_revenue_estimate(page):
    await page.wait_for_selector('section[data-testid="revenueEstimate"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    revenue_section = soup.find('section', {'data-testid': 'revenueEstimate'})
    
    if revenue_section:
        print("Found Revenue Estimate section")
        
        # Extract table data
        table = revenue_section.find('table')
        if table:
            headers = [th.text for th in table.find_all('th')]
            
            data_rows = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                data = [col.text for col in columns]
                data_rows.append(data)
            
            # Create a DataFrame
            df = pd.DataFrame(data_rows[1:], columns=headers)
            return df
    return pd.DataFrame()

async def fetch_eps_trend(page):
    await page.wait_for_selector('section[data-testid="epsTrend"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    eps_section = soup.find('section', {'data-testid': 'epsTrend'})
    
    if eps_section:
        print("Found EPS Trend section")
        
        # Extract table data
        table = eps_section.find('table')
        if table:
            headers = [th.text for th in table.find_all('th')]
            
            data_rows = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                data = [col.text for col in columns]
                data_rows.append(data)
            
            # Create a DataFrame
            df = pd.DataFrame(data_rows[1:], columns=headers)
            return df
    return pd.DataFrame()

async def fetch_growth_estimate(page):
    await page.wait_for_selector('section[data-testid="growthEstimate"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    growth_section = soup.find('section', {'data-testid': 'growthEstimate'})
    
    if growth_section:
        print("Found Growth Estimate section")
        
        # Extract table data
        table = growth_section.find('table')
        if table:
            headers = [th.text for th in table.find_all('th')]
            
            data_rows = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                data = [col.text for col in columns]
                data_rows.append(data)
            
            # Create a DataFrame
            df = pd.DataFrame(data_rows[1:], columns=headers)
            return df
    return pd.DataFrame()

async def fetch_top_analysts(page):
    await page.wait_for_selector('section#top-analyst')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    analysts_section = soup.find('section', {'id': 'top-analyst'})
    
    if analysts_section:
        print("Found Top Analysts section")
        
        # Extract table data
        table = analysts_section.find('table')
        if table:
            headers = [th.text for th in table.find_all('th')]
            
            data_rows = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                data = [col.text for col in columns]
                data_rows.append(data)
            
            # Create a DataFrame
            df = pd.DataFrame(data_rows[1:], columns=headers)
            return df
    return pd.DataFrame()

async def fetch_revenue_earnings(page):
    await page.wait_for_selector('section[data-testid="revenue-earnings-chart"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    revenue_earnings_section = soup.find('section', {'data-testid': 'revenue-earnings-chart'})
    
    if revenue_earnings_section:
        print("Found Revenue vs. Earnings section")
        
        # Extract the quarterly data
        quarters = revenue_earnings_section.find_all('div', class_='tick yf-58fx9d')
        quarter_names = [quarter.find('div', class_='text yf-58fx9d').text for quarter in quarters]
        
        groups = revenue_earnings_section.find_all('g', class_=['group yf-eykbat', 'group selected yf-eykbat'])
        data_rows = []
        for i, group in enumerate(groups):
            revenue_value = group.find('rect', class_='rect-one yf-eykbat')['data-value']
            earnings_value = group.find('rect', class_='rect-two yf-eykbat')['data-value']
            quarter_name = quarter_names[i] if i < len(quarter_names) else f"Quarter {i + 1}"
            data_rows.append([quarter_name, revenue_value, earnings_value])
        
        # Create a DataFrame
        df = pd.DataFrame(data_rows, columns=['Quarter', 'Revenue', 'Earnings'])
        return df
    return pd.DataFrame()

async def fetch_analyst_price_targets(page):
    await page.wait_for_selector('section[data-testid="analyst-price-target-card"]')
    html_content = await page.content()

    soup = BeautifulSoup(html_content, 'html.parser')
    price_target_section = soup.find('section', {'data-testid': 'analyst-price-target-card'})
    
    if price_target_section:
        print("Found Analyst Price Targets section")
        
        current_price_container = price_target_section.find('div', class_='priceContainer current yf-1i34qte')
        current_price = current_price_container.find('span', class_='price yf-1i34qte').text if current_price_container else "No current price found"
        
        average_price_container = price_target_section.find('div', class_='priceContainer average yf-1i34qte')
        average_price = average_price_container.find('span', class_='price yf-1i34qte').text if average_price_container else "No average price found"
        
        data = {'Current Price': [current_price], 'Average Price': [average_price]}
        df = pd.DataFrame(data)
        return df
    return pd.DataFrame()

async def fetch_earnings_history(page):
    await page.wait_for_selector('section[data-testid="earningsHistory"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    earnings_history_section = soup.find('section', {'data-testid': 'earningsHistory'})
    
    if earnings_history_section:
        print("Found Earnings History section")
        
        # Extract table data
        table = earnings_history_section.find('table')
        if table:
            headers = [th.text for th in table.find_all('th')]
            
            data_rows = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                data = [col.text for col in columns]
                data_rows.append(data)
            
            # Create a DataFrame
            df = pd.DataFrame(data_rows, columns=headers)
            return df
    return pd.DataFrame()

async def getData(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/analysis/'
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url, timeout=60000)
        
        earnings_df = await fetch_earnings_estimate(page)
        revenue_df = await fetch_revenue_estimate(page)
        earnings_his = await fetch_earnings_history(page)
        eps_trend_df = await fetch_eps_trend(page)
        growth_estimate_df = await fetch_growth_estimate(page)
        top_analysts_df = await fetch_top_analysts(page)
        revenue_earnings_df = await fetch_revenue_earnings(page)
        analyst_price_targets_df = await fetch_analyst_price_targets(page)
        
        # Return the DataFrames
        return {
            'earnings_df': earnings_df,
            'revenue_df': revenue_df,
            'earnings_history': earnings_his,
            'eps_trend_df': eps_trend_df,
            'growth_estimate_df': growth_estimate_df,
            'top_analysts_df': top_analysts_df,
            'revenue_earnings_df': revenue_earnings_df,
            'analyst_price_targets_df': analyst_price_targets_df
        }

async def main(ticker):
    data = await getData(ticker)
    return data
