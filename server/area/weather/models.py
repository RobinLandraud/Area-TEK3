from django.db import models

# Create your models here.

#actual meteo data
class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    wind_deg = models.FloatField()
    clouds_all = models.FloatField()
    weather_id = models.FloatField()
    weather_main = models.CharField(max_length=100)
    weather_description = models.CharField(max_length=100)
    weather_icon = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city