from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ticker = 'AAPL'
url = f'https://finance.yahoo.com/quote/{ticker}/'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Fetch the main page
    page.goto(url)
    
    # Click the "News" button
    page.click('button#tab-latest-news')  # Adjust the selector based on the actual HTML
    
    # Wait for the news section to load
    page.wait_for_selector('section.stream-items')
    html_content = page.content()
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    news_section = soup.find('section', class_='stream-items small layoutCol2 autoCol yf-1x0cgbi')
    a_tags = news_section.find_all('a')
    
    links = [a_tag.get('href') for a_tag in a_tags if a_tag.get('href') and 'news' in a_tag.get('href')]
    print(links)
    
    # Fetch each article page within the same browser session
    for link in links:
        article_url = link if link.startswith('http') else f'https://finance.yahoo.com{link}'
        
        page.goto(article_url)
        page.wait_for_selector('h1')  # Wait for the article title to load
        article_html_content = page.content()
        
        # Use BeautifulSoup to parse the article HTML content
        article_soup = BeautifulSoup(article_html_content, 'html.parser')
        
        title_tag = article_soup.find('h1', class_='cover-title yf-1o1tx8g')
        
        if title_tag:
            title = title_tag.text
            print(f'Title: {title}')
            print('---')
    
    browser.close()