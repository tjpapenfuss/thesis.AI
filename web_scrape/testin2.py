import requests
from bs4 import BeautifulSoup

# Replace this URL with the one you want to parse
url = 'https://aws.amazon.com/solutions/case-studies/caremonitor/'

response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

elements = soup.find_all(['h1', 'h2', 'h3', 'p'])

for element in elements:
    text = element.get_text(strip=True)
    print(text)
    print('=' * 40)