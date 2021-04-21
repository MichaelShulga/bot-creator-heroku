import requests

url = 'https://api.heroku.com/regions/Europe'

headers = {"Content-Type": "application/json",
           "Accept": "application/vnd.heroku+json; version=3",
           "Authorization": "Bearer 5d5bd4df-8111-46ce-8adf-741997a82e78"}
res = requests.get(url, headers=headers)

print(res.json())
