import asyncio
import requests
import json

def get_weather(city: str):
    API_KEY = '3417a2349abdc7bccb31c3b73b88ca0f'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = json.loads(response.text)
    return data

if __name__ == '__main__':
    print(get_weather('Bordeaux'))