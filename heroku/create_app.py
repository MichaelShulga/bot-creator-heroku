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
           "Authorization": "Bearer 5d5bd4df-8111-46ce-8adf-741997a82e78"}
res = requests.post(url, json=payload, headers=headers)
print(res.json())