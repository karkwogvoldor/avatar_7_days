import requests

url = 'https://last-airbender-api.fly.dev/api/v1/characters'
response = requests.get(url)
print(response.json())