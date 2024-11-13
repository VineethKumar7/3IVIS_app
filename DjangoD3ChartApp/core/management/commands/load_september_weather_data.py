# core/management/commands/load_september_weather_data.py

import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import WeatherData

class Command(BaseCommand):
    help = 'Load weather data for September from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'september_weather.csv')
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                WeatherData.objects.create(
                    date=row['date'],
                    temperature=row['temperature'],
                    humidity=row['humidity']
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded weather data for September'))
