import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio

ticker = 'AAPL'
url = f'https://finance.yahoo.com/quote/{ticker}/analysis/'

async def fetch_earnings_estimate(page):
    await page.wait_for_selector('section[data-testid="earningsEstimate"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    earnings_section = soup.find('section', {'data-testid': 'earningsEstimate'})
    
    if earnings_section:
        print("Found Earnings Estimate section")
        
        # Extract the title
        title_tag = earnings_section.find('h3', class_='header')
        title = title_tag.text if title_tag else "No title found"
        print(f'Title: {title}')
        
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
            print(df)
        else:
            print("No table found")
    else:
        print("Earnings Estimate section not found")

async def fetch_revenue_estimate(page):
    await page.wait_for_selector('section[data-testid="revenueEstimate"]')
    html_content = await page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    revenue_section = soup.find('section', {'data-testid': 'revenueEstimate'})
    
    if revenue_section:
        print("Found Revenue Estimate section")
        
        # Extract the title
        title_tag = revenue_section.find('h3', class_='header')
        title = title_tag.text if title_tag else "No title found"
        print(f'Title: {title}')
        
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
            print(df)
        else:
            print("No table found")
    else:
        print("Revenue Estimate section not found")

async def fetch_eps_trend(page):
    await page.wait_for_selector('section[data-testid="epsTrend"]')
    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    eps_section = soup.find('section', {'data-testid': 'epsTrend'})
    table = eps_section.find('table')
    
    if table:
        headers = [th.text for th in table.find_all('th')]
        data_rows = []
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            data = [col.text for col in columns]
            data_rows.append(data)
        
        df = pd.DataFrame(data_rows[1:], columns=headers)
        print("EPS Trend:")
        print(df)
    else:
        print("No EPS Trend table found")

async def fetch_growth_estimate(page):
    await page.wait_for_selector('section[data-testid="growthEstimate"]')
    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    growth_section = soup.find('section', {'data-testid': 'growthEstimate'})
    table = growth_section.find('table')
    
    if table:
        headers = [th.text for th in table.find_all('th')]
        data_rows = []
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            data = [col.text for col in columns]
            data_rows.append(data)
        
        df = pd.DataFrame(data_rows[1:], columns=headers)
        print("Growth Estimate:")
        print(df)
    else:
        print("No Growth Estimate table found")

async def fetch_top_analysts(page):
    await page.wait_for_selector('section#top-analyst')
    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    analysts_section = soup.find('section', {'id': 'top-analyst'})
    table = analysts_section.find('table')
    
    if table:
        headers = [th.text for th in table.find_all('th')]
        data_rows = []
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            data = [col.text for col in columns]
            data_rows.append(data)
        
        df = pd.DataFrame(data_rows[1:], columns=headers)
        print("Top Analysts:")
        print(df)
    else:
        print("No Top Analysts table found")
        
# async def fetch_earnings_report(page):
#     await page.wait_for_selector('div.content.yf-qdsu8q')
#     container = await page.query_selector('div.chart.yf-qdsu8q')
#     await container.scroll_into_view_if_needed()
    
#     # Get the bounding boxes of the circles
#     circles = await page.query_selector_all('div.chart.yf-qdsu8q canvas')
#     bounding_boxes = [await circle.bounding_box() for circle in circles]
    
#     for i, bounding_box in enumerate(bounding_boxes):
#         # Calculate the coordinates to move the mouse to the right of each rectangle
#         x = bounding_box['x'] + bounding_box['width'] - 1
#         y = bounding_box['y'] + bounding_box['height'] / 2
#         print(f"Moving mouse to ({x}, {y})")
        
#         # Move the mouse to the calculated coordinates
#         await page.mouse.move(x, y, steps=10)
#         await page.wait_for_timeout(500)  # Wait for the tooltip to appear
        
#         actual = await page.query_selector('div[title="Actual"] span.txt-positive')
#         estimate = await page.query_selector('div[title="Estimate"] span.txt-positive')
        
#         if estimate:
#             estimate_value = float((await estimate.inner_text()).replace('+', ''))
#             if actual:
#                 actual_value = float((await actual.inner_text()).replace('+', ''))
#                 difference = actual_value - estimate_value
#                 result = "Beat" if difference > 0 else "Missed"
#                 print(f"Earnings Report {i + 1}: Actual = {actual_value}, Estimate = {estimate_value}, Difference = {difference}, Result = {result}")
#             else:
#                 print(f"Earnings Report {i + 1}: Estimate = {estimate_value}, Actual value not found")
#         else:
#             print(f"Earnings Report {i + 1}: Estimate value not found")

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
        
        groups = revenue_earnings_section.find_all('g', class_=['group yf-si65b', 'group selected yf-si65b'])
        for i, group in enumerate(groups):
            revenue_value = group.find('rect', class_='rect-one yf-si65b')['data-value']
            earnings_value = group.find('rect', class_='rect-two yf-si65b')['data-value']
            quarter_name = quarter_names[i] if i < len(quarter_names) else f"Quarter {i + 1}"
            print(f'{quarter_name}: Revenue = {revenue_value}, Earnings = {earnings_value}')
    else:
        print("Revenue vs. Earnings section not found")
        
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url)
        
        await asyncio.gather(
            # fetch_earnings_estimate(page),
            # fetch_revenue_estimate(page),
            # fetch_eps_trend(page),
            # fetch_growth_estimate(page),
            # fetch_top_analysts(page),
            # fetch_earnings_report(page)
            fetch_revenue_earnings(page)
        )
        
        await browser.close()

asyncio.run(main())