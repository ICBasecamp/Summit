from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import pandas as pd
import json

async def fetch_bluesky(query: str, limit: int = 10):
    url = f'https://bsky.app/search?q={query}'
    posts = []

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
            
            # Extract the divs with the class 'css-146c3p1' and data-testid 'postText'
            tweets = soup.find_all('div', class_='css-146c3p1', attrs={'data-testid': 'postText'}, limit=limit)
            if tweets:
                for tweet in tweets:
                    content = tweet.text.strip()
                    post_data = {'Content': content}
                    
                    # Check for images in the post
                    image_div = tweet.find_next('div', class_='css-175oi2r')
                    if image_div:
                        img_tag = image_div.find('img')
                        if img_tag and 'src' in img_tag.attrs:
                            post_data['Image'] = img_tag['src']
                    
                    posts.append(post_data)
                    
        except Exception as e:
            print(f"Failed to fetch content {url}: {e}")
        finally:
            await page.close()

    return posts
