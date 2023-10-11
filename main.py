import requests
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

city_name = 'Olsztyn'
url = f'https://www.meteoprog.pl/pl/weather/{city_name}'
response = requests.get(url)

if response.status_code != 200:
    assert False

soup = BeautifulSoup(response.content, features='html.parser')
table = soup.find('ul', class_='today-hourly-weather').findAll("li")


for row in table:
    name = row.find('span', class_='today-hourly-weather__name').text.strip()
    temp = row.find('span', class_='today-hourly-weather__temp').text.strip()
    feel = row.find('span', class_='today-hourly-weather__feel').text.strip()
    print(name, temp, feel)
