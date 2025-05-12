'''Simple python file to pull data from an API and write to a csv.'''
import requests
import pandas as pd
from datetime import datetime, timezone
import csv
import os

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

def get_data_from_latlon(lat, lon):
    '''Make a request to https://home.openweathermap.org/'''
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}")
    return response.json()

def transform_data(data):
    '''Take a dict of raw weather data and process it.'''
    weather = data['weather'][0]
    weather['utctime'] = datetime.now(timezone.utc).strftime('%Y/%m/%d-%H:%M')
    weather['wind_speed'] = data['wind']['speed']
    weather['wind_dir'] = data['wind']['deg']    
    main_fields = ['humidity','feels_like','temp_min','temp_max']
    for field in main_fields:
        weather[field] = data['main'][field]
    weather.pop('main')
    weather.pop('icon')
    weather.pop('id')
    return weather

if __name__ == '__main__':
    LATITUDE = 51.444124
    LONGITUDE = -2.564519

    data = get_data_from_latlon(LATITUDE, LONGITUDE)
    weather = transform_data(data)
    with open("out.csv", "w", newline="") as f:
        w = csv.DictWriter(f, weather.keys())
        w.writeheader()
        w.writerow(weather)



 