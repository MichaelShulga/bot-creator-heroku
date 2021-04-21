import uuid
import requests

url = 'https://api.heroku.com/apps'

name = f'test-{str(uuid.uuid4())[:8]}'
print(name)

payload = {
    "name": name,
    "region": "eu"
}
headers = {"Content-Type": "application/json",
           "Accept": "application/vnd.heroku+json; version=3",
           "Authorization": 'Basic anVkb3NodWxnYUBnbWFpbC5jb206Q1VmdVR6Xj9QcWpOY243'}
res = requests.post(url, json=payload, headers=headers)
print(res.json())