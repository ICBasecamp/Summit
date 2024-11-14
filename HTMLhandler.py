from bs4 import BeautifulSoup
import httpx

ticker = 'CSCO'
url = f'https://finance.yahoo.com/quote/{ticker}/'
html_content = httpx.get(url).text

soup = BeautifulSoup(html_content, 'html.parser')
news_section = soup.find('section', class_='stream-items small layoutCol2 autoCol yf-1x0cgbi')
a_tags = news_section.find_all('a')

links = [a_tag.get('href') for a_tag in a_tags if a_tag.get('href') and 'news' in a_tag.get('href')]

for link in links:
    article_url = link if link.startswith('http') else f'https://finance.yahoo.com{link}'
    article_html_content = httpx.get(article_url).text
    article_soup = BeautifulSoup(article_html_content, 'html.parser')
    
    title_tag = article_soup.find('h1', class_='cover-title yf-1o1tx8g')
    
    if title_tag:
        title = title_tag.text
        print(f'Title: {title}')
        print(f'Link: {article_url}')
        print('---')