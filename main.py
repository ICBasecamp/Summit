from bs4 import BeautifulSoup
import requests

url = 'https://finance.yahoo.com/quote/CSCO/'
html_content = requests.get(url).text

soup = BeautifulSoup(html_content, 'html.parser')
news_section = soup.find('section', class_='stream-items small layoutCol2 autoCol yf-1x0cgbi')
a_tags = news_section.find_all('a')

for a_tag in a_tags:
    print(a_tag.get('href'))
