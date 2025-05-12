import secrets
import requests

if __name__ == '__main__':
    API_KEY = ''
    LATITUDE = 51.444124
    LONGITUDE = -2.564519

    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}")
    data = response.json()

    print(data)
    