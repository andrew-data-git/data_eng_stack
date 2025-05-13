'''Simple python file to pull data from an API and write to a csv.'''
import requests
import pandas as pd
from datetime import datetime, timezone
import csv
import os
import psycopg2

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

def get_data_from_latlon(lat, lon):
    '''Make a request to https://home.openweathermap.org/, return the json response'''
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}")
    return response.json()

def transform_data(data):
    '''Take a dict of raw weather data and process it to another dict.'''
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
    
def insert_weather_data(weather_data):
    '''For processed weather info, insert into weather table.'''
    cursor.execute( #TODO on conflict do nothing
        """
        INSERT INTO weather (
            description,
            utctime,
            wind_speed,
            wind_dir,
            humidity,
            feels_like,
            temp_min,
            temp_max
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            weather_data['description'],
            weather_data['utctime'],
            weather_data['wind_speed'],
            weather_data['wind_dir'],
            weather_data['humidity'],
            weather_data['feels_like'],
            weather_data['temp_min'],
            weather_data['temp_max']
        )
    )
    conn.commit()

def query_tail_of_table(table, id):
    """Query table for testing purposes."""
    res = cursor.execute(
        f"""
        SELECT * FROM {table} ORDER BY {id} DESC LIMIT 5
        """
    )
    rows = cursor.fetchall()
    for row in rows:
        print(row)

if __name__ == '__main__':
    LATITUDE = 51.444124
    LONGITUDE = -2.564519

    data = get_data_from_latlon(LATITUDE, LONGITUDE)
    weather_data = transform_data(data) # a dict of transformed weather data

    # create postgres cursor
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="localhost", # weather_db
        port="5432"
    )
    cursor = conn.cursor()

    # make table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
            utctime TEXT NOT NULL PRIMARY KEY,
            description TEXT NOT NULL,
            wind_speed FLOAT,
            wind_dir INT,
            humidity INT,
            feels_like FLOAT,
            temp_min FLOAT,
            temp_max FLOAT
        );
        """
    )

    # insert data
    insert_weather_data(weather_data)

    # query
    query_tail_of_table('weather', 'utctime')

    cursor.close()
    conn.close()



 