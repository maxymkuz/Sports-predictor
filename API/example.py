import requests

url = "http://maxkuz.pythonanywhere.com/"

home_team = "Man City"
away_team = "Chelsea"
profit = 3.5

response = requests.get(url + f"{home_team}/{away_team}/{profit}")

data = response.json()

print(data)
