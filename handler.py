import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

import pandas as pd

ticker = 'AAPL'
url = f'https://finance.yahoo.com/quote/{ticker}/'

async def fetch_article(browser, link):
    article_url = link if link.startswith('http') else f'https://finance.yahoo.com{link}'
    page = await browser.new_page()
    print(f"Fetching article: {article_url}")
    
    try:
        await page.goto(article_url, timeout=60000)  # Increase timeout to 60 seconds
        print(f"Loaded article: {article_url}")
        
        # Grab the title before clicking the "Continue Reading" button
        article_html_content = await page.content()
        article_soup = BeautifulSoup(article_html_content, 'html.parser')
        title_tag = article_soup.find('h1', class_='cover-title yf-1o1tx8g')
        title = title_tag.text if title_tag else "No title found"
        
        # Check for "Continue Reading" button and click it if present
        try:
            # await page.wait_for_selector('button[aria-label="Continue Reading"]', timeout=10000)
            await page.click('button[aria-label="Continue Reading"]')
            print(f"Clicked 'Continue Reading' button for: {article_url}")
            
            # Fetch the content from <p> tags after clicking the button
            article_html_content = await page.content()
            article_soup = BeautifulSoup(article_html_content, 'html.parser')
            content_tags = article_soup.find_all('p')
            content = "\n".join(tag.text for tag in content_tags)
        except Exception as e:
            print(f"No 'Continue Reading' button for: {article_url} - {e}")
            
            # Fetch the content from <p> tags within the "article-wrap no-bb" class
            article_html_content = await page.content()
            article_soup = BeautifulSoup(article_html_content, 'html.parser')
            article_wrap = article_soup.find('div', class_='article-wrap no-bb')
            if article_wrap:
                content_tags = article_wrap.find_all('p')
                content = "\n".join(tag.text for tag in content_tags)
            else:
                content = "No content found"
        
        print(f'Title: {title}')
        # print(f'Content: {content}')
        print(f'Link: {article_url}')
        print('---')

        return {'Title': title, 'Content': content, 'Link': article_url}

    except Exception as e:
        print(f"Failed to fetch article {article_url}: {e}")
        return {'Title': "Error", 'Content': "Error", 'Link': article_url}
    finally:
        await page.close()

async def fetch(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/'
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Fetch the main page
        await page.goto(url)
        print("Loaded main page")
        
        # Click the "News" button
        await page.click('button#tab-latest-news')  # Adjust the selector based on the actual HTML
        print("Clicked 'News' button")
        
        # Wait for the news section to load
        await page.wait_for_selector('section.stream-items')
        print("News section loaded")
        
        await page.wait_for_selector('div.yf-gfq5ju')
        html_content = await page.content()
        
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        news_section = soup.find('section', class_='stream-items small layoutCol2 autoCol yf-1x0cgbi')
        a_tags = news_section.find_all('a')
        
        # Use a set to store unique links
        links = set(a_tag.get('href') for a_tag in a_tags if a_tag.get('href') and 'news' in a_tag.get('href'))
        print(f"Found {len(links)} unique links")


        
        tasks = [fetch_article(browser, link) for link in links]
        results = await asyncio.gather(*tasks)
        
        await browser.close()
        
        df = pd.DataFrame(results, columns=['Title', 'Content', 'Link'])
        return df
    
# Temporarily remove the asyncio.run() call to avoid running the script automatically
# async def main():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()
        
#         # Fetch the main page
#         await page.goto(url)
#         print("Loaded main page")
        
#         # Click the "News" button
#         await page.click('button#tab-latest-news')  # Adjust the selector based on the actual HTML
#         print("Clicked 'News' button")
        
#         # Wait for the news section to load
#         await page.wait_for_selector('section.stream-items')
#         print("News section loaded")
        
#         await page.wait_for_selector('div.yf-gfq5ju')
#         html_content = await page.content()
        
#         # Use BeautifulSoup to parse the HTML content
#         soup = BeautifulSoup(html_content, 'html.parser')
#         news_section = soup.find('section', class_='stream-items small layoutCol2 autoCol yf-1x0cgbi')
#         a_tags = news_section.find_all('a')
        
#         # Use a set to store unique links
#         links = set(a_tag.get('href') for a_tag in a_tags if a_tag.get('href') and 'news' in a_tag.get('href'))
#         print(f"Found {len(links)} unique links")
        
#         tasks = [fetch_article(browser, link) for link in links]
#         await asyncio.gather(*tasks)
        
#         await browser.close()
        
        
# asyncio.run(main())
