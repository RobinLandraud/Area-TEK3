from .models import Weather
from .api import get_weather
from django.utils import timezone
from datetime import timedelta

import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth.models import OAuthToken
from django.contrib.auth.models import User
from services.functions import callReaction

import requests

def update_weather_info():
    # Get the weather info from the API
    updated = False
    weather_info = get_weather('Bordeaux')
    #print time
    print(f"[{str(timezone.now())}]")
    # Create a new weather object with the data
    print("[WEATHER CRON]: Creating new weather data")
    Weather.objects.create(
        city=f"{weather_info['name']} {str(timezone.now())}",
        temperature=weather_info['main']['temp'],
        feels_like=weather_info['main']['feels_like'],
        temp_min=weather_info['main']['temp_min'],
        temp_max=weather_info['main']['temp_max'],
        pressure=weather_info['main']['pressure'],
        humidity=weather_info['main']['humidity'],
        wind_speed=weather_info['wind']['speed'],
        wind_deg=weather_info['wind']['deg'],
        clouds_all=weather_info['clouds']['all'],
        weather_id=weather_info['weather'][0]['id'],
        weather_main=weather_info['weather'][0]['main'],
        weather_description=weather_info['weather'][0]['description'],
        weather_icon=weather_info['weather'][0]['icon'],
    )
    print("[WEATHER CRON]: Done creating new weather data")
    print("[WEATHER CRON]: Deleting old weather data")
    while Weather.objects.count() > 10:
        Weather.objects.all()[0].delete()
    print("[WEATHER CRON]: Done deleting old weather data")
    if Weather.objects.count() > 1:
        diff_temp = Weather.objects.all()[Weather.objects.count()-1].temperature - Weather.objects.all()[Weather.objects.count()-2].temperature
        if diff_temp > 0:
            print("[WEATHER CRON]: Temperature is rising")
            updated = True
        elif diff_temp < 0:
            print("[WEATHER CRON]: Temperature is falling")
            updated = True
        else:
            print("[WEATHER CRON]: Temperature is stable")
    if updated:
        users = User.objects.all()
        for user in users:
            callReaction("AWE0", user)