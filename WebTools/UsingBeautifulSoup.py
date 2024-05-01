from bs4 import BeautifulSoup as bs
import requests

url = 'http://bing.com'
req = requests.get(url)
tree = bs(req.text, 'html.parser')
for link in tree.find_all('a'):
    print(f"{link.get('href')} -> {link.text}")

