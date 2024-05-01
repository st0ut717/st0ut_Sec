from io import BytesIO
from lxml import etree
import requests

url = 'https://fairoaksit.com'
req = requests.get(url)
content = req.content

parser = etree.HTMLParser()
content = etree.parse(BytesIO(content), parser=parser)
for link in content.findall('//a'):
    print(f"{link.get('href')} -> {link.text}")
