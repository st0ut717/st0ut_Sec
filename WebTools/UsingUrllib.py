import urllib.parse
import urllib.request
url = 'https://www.fairoaksit.com'
with urllib.request.urlopen(url) as responce:
    content = responce.read()

print(content)
