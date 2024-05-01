import requests
url = 'https://www.boodelyboo.com'

responce = requests.get(url)
data = {
        'user': 'tim',
        'passwd': '31337'
        }
responce = requests.post(url, data=data)
print(responce.text)
print(responce.content)
