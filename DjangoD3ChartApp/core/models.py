# core/models.py

from django.db import models

class WeatherData(models.Model):
    date = models.DateField()  # Date of the weather record
    temperature = models.DecimalField(max_digits=5, decimal_places=2)  # Temperature in Celsius
    humidity = models.DecimalField(max_digits=5, decimal_places=2)  # Humidity in percentage
    # Add other fields as needed

    def __str__(self):
        return f"Weather on {self.date}: {self.temperature}°C, {self.humidity}% Humidity"
