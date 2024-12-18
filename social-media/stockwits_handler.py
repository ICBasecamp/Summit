from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import pandas as pd
import asyncio
import json

async def fetch_stockwits(symbol: str, limit: int = 20):
    url = f'https://stocktwits.com/symbol/{symbol}'
    posts = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"Fetching content: {url}")
        
        try:
            await page.goto(url, timeout=60000)
            print(f"Loaded content: {url}")
            
            # Click the "Popular" tab
            try:
                await page.click('li[aria-controls="panel:r0:1"]')
                print("Clicked 'Popular' tab")
            except Exception as e:
                print("No 'Popular' tab found, skipping...")
            
            await page.wait_for_selector('div.infinite-scroll-component', timeout=60000)
            content_html = await page.content()
            soup = BeautifulSoup(content_html, 'html.parser')
            
            # Extract the divs with the class 'StreamMessage_container__omTCg'
            messages = soup.find_all('div', class_='StreamMessage_container__omTCg', limit=limit)
            if messages:
                for message in messages:
                    content = message.find('div', class_='RichTextMessage_body__4qUeP').text.strip()
                    post_data = {'Content': content}
                    
                    # Check for images in the post
                    image_div = message.find('div', class_='StreamMessage_avatarImage__e5N6L')
                    if image_div:
                        img_tag = image_div.find('img')
                        if img_tag and 'src' in img_tag.attrs:
                            post_data['Image'] = img_tag['src']
                    
                    posts.append(post_data)
                    
        except Exception as e:
            print(f"Failed to fetch content {url}: {e}")
        finally:
            await page.close()

    # Save the results to a JSON file
    with open('social-media/results/stockwits_posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

    return posts