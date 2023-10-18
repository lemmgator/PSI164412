import json
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import datetime


# 1)

def check_url(url: str) -> bool:
    response = requests.get(url)
    if response.status_code >= 200 or response.status_code <= 299:
        return True
    assert False


url = 'http://wmii.uwm.edu.pl'
response = requests.get(url)

print(check_url(url))


# 2)

def check_temp(city_name: str):
    url = f'https://www.meteoprog.pl/pl/weather/{city_name}/'
    response = requests.get(url)

    if response.status_code != 200:
        assert False

    soup = BeautifulSoup(response.content, features='html.parser')
    table = soup.find('ul', class_="today-hourly-weather")
    temp = table.find_all('span', class_="today-hourly-weather__temp")
    name = table.find_all('span', class_="today-hourly-weather__name")
    tp = []
    nm = []
    for row in temp:
        tp.append(row.getText())
    tp = [int(t.replace('°', '').replace('+', '')) for t in tp]
    for row in name:
        nm.append(row.get_text())
    plt.plot(nm, tp)
    plt.ylabel('Temperatura (°C)')
    plt.xlabel('Czas')
    plt.title("Temperatura - " + city_name)
    plt.show()


check_temp("Olsztyn")


# 3)

def check_sensor(sensor_id):
    url = f'https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}'
    response = requests.get(url)
    content = response.content.decode('utf-8')
    parsed_content = json.loads(content)
    dates = []
    values = []
    for entry in parsed_content['values']:
        if entry['value']:
            dates.append(datetime.datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S'))
            values.append(entry['value'])
    return plt.plot(dates, values, label=parsed_content['key'])


def check_station(station_id, param):
    url = f'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}'
    response = requests.get(url)
    content = response.content.decode('utf-8')
    parsed_content = json.loads(content)
    for i in parsed_content:
        for j in param:
            if i['param']['paramCode'] == j:
                check_sensor(i['id'])
    plt.xlabel('Data')
    plt.ylabel('Wartość')
    plt.title('Wykres danych')
    plt.legend()
    plt.xticks(rotation=30)
    plt.show()


check_station(877, ["NO2", "PM10", "PM2.5", "SO2"])
