from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

import requests
import asyncio

async def fetch_bsky_uri_cid(post_url: str):
    collection = "app.bsky.feed.post",

    # Extract repo and rkey from URL format: /profile/{repo}/post/{rkey}
    parts = post_url.strip('/').split('/')
    if len(parts) >= 4 and parts[0] == 'profile' and parts[2] == 'post':
        repo = parts[1]
        rkey = parts[3]

    if not repo or not rkey:
        raise Exception(f"Invalid Bluesky post URL: {post_url}")
    
    params = {
        "repo": repo,
        "rkey": rkey,
        "collection": collection
    }

    response = requests.get('https://bsky.social/xrpc/com.atproto.repo.getRecord', params=params)

    if response.status_code == 200:
        data = response.json()
        return data['uri'], data['cid']
    else:
        raise Exception(f"Failed to fetch URI CID for post {post_url}")

    

    

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
            tweets = soup.find_all('div', class_='css-175oi2r r-18u37iz r-uaa2di', limit=limit)
            # tweets = soup.find_all('div', class_='css-146c3p1', attrs={'data-testid': 'postText'}, limit=limit)

            bsky_embeddings = []

            if tweets:
                for tweet in tweets:
                    embedding_data = {} 

                    content = tweet.find('div', class_='css-146c3p1', attrs={'data-testid': 'postText'})
                    text_content = content.text.strip()
                    post_data = {'Content': text_content, 'Source': 'Bluesky'}

                    post_link = tweet.find('a', class_="css-146c3p1 r-1loqt21", href=True)['href']
                    uri, cid = await fetch_bsky_uri_cid(post_link)

                    embedding_data['URI'] = uri
                    embedding_data['CID'] = cid
                    
                    # Check for images in the post
                    image_div = content.find_next('div', class_='css-175oi2r')
                    if image_div:
                        img_tag = image_div.find('img')
                        if img_tag and 'src' in img_tag.attrs:
                            post_data['Image'] = img_tag['src']
                    
                    posts.append(post_data)
                    bsky_embeddings.append(embedding_data)
                    
        except Exception as e:
            print(f"Failed to fetch content {url}: {e}")
        finally:
            # print(posts)
            await page.close()

    return posts, bsky_embeddings

asyncio.run(fetch_bluesky('NVDA stock', limit=5))
