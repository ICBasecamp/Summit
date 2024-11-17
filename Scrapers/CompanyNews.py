import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import httpx

ticker = 'AAPL'
url = f'https://finance.yahoo.com/quote/{ticker}/'

async def fetch_article(client, link):
    article_url = link if link.startswith('http') else f'https://finance.yahoo.com{link}'
    response = await client.get(article_url)
    article_html_content = response.text
    article_soup = BeautifulSoup(article_html_content, 'html.parser')
    title_tag = article_soup.find('h1', class_='cover-title yf-1o1tx8g')
    
    if title_tag:
        title = title_tag.text
        print(f'Title: {title}')
        print(f'Link: {article_url}')
        print('---')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Fetch the main page
        await page.goto(url)
        
        # Click the "News" button
        await page.click('button#tab-latest-news')  # Adjust the selector based on the actual HTML
        
        # Wait for the news section to load
        await page.wait_for_selector('section.stream-items')
        html_content = await page.content()
        
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        news_section = soup.find('section', class_='stream-items small layoutCol2 autoCol yf-1x0cgbi')
        a_tags = news_section.find_all('a')
        
        # Use a set to store unique links
        links = set(a_tag.get('href') for a_tag in a_tags if a_tag.get('href') and 'news' in a_tag.get('href'))
        
        async with httpx.AsyncClient() as client:
            tasks = [fetch_article(client, link) for link in links]
            await asyncio.gather(*tasks)
        
        await browser.close()

asyncio.run(main())