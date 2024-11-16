import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def fetch_bluesky(query: str, limit: int = 10):
    url = f'https://bsky.app/search?q={query}'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"Fetching content: {url}")
        
        try:
            await page.goto(url, timeout=60000)
            print(f"Loaded content: {url}")
            
            await page.wait_for_selector('div.css-146c3p1[data-testid="postText"]', timeout=60000)
            content_html = await page.content()
            soup = BeautifulSoup(content_html, 'html.parser')
            
            # Extract the first div with the class 'css-175oi2r' inside the specified XPath
            tweets = soup.find_all('div', class_='css-146c3p1', attrs={'data-testid': 'postText'}, limit=limit)
            if tweets:
                for tweet in tweets:
                    content = tweet.text.strip()
                    print(f'Content: {content}')
                    print('---')

        except Exception as e:
            print(f"Failed to fetch content {url}: {e}")
        finally:
            await page.close()

# Test Execution
asyncio.run(fetch_bluesky('AMZN', 3))