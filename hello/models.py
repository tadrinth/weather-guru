from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import datetime
import json
import requests
import decimal
import logging

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)
	
class City(models.Model):
	api_id = models.IntegerField()
	name = models.CharField(max_length=100)
	subscribers = models.ManyToManyField(User)
	# cached = models.CharField(max_length=1000,default="")
	weather = models.CharField(max_length=100,default="Unknown")
	temperature = models.IntegerField(default=290)
	modified_date = models.DateTimeField(auto_now=True)
	low_temperature_tomorrow = models.IntegerField(default=290) 
	high_temperature_tomorrow = models.IntegerField(default=290) 
	
	def get_details(self):
		if(timezone.now() - self.modified_date > datetime.timedelta(minutes=10)):
			try:
				result = json.loads(self.pull_from_api())
				if "weather" in result:
					self.weather = ", ".join(map(lambda x: x["main"], result["weather"]))
				if "name" in result:
					self.name = result["name"]
				if "main" in result:
					self.temperature = round(float(result["main"]["temp"]))
					
					
				forecast = json.loads(self.get_forecast())
				if "list" in forecast:
					tomorrow = forecast["list"][9]
					self.low_temperature_tomorrow = round(float(tomorrow["main"]["temp_min"]))
					self.high_temperature_tomorrow = round(float(tomorrow["main"]["temp_max"]))
				
				self.save()
			except:
				logger = logging.getLogger(__name__)
				logger.error("Failed to read from API")
		
	def pull_from_api(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?id=" + str(self.api_id) + "&appid=cdfdac6c8b96346016dea9fa93d524b6")
		return r.content
	
	def get_forecast(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=" + str(self.api_id) + "&appid=cdfdac6c8b96346016dea9fa93d524b6")
		return r.content
	
	def temperature_in_f(self):
		return self.k2f(self.temperature)

	def tomorrow(self):
		return "Tomorrow: " + str(self.k2f(self.low_temperature_tomorrow)) + "-" + str(self.k2f(self.high_temperature_tomorrow)) + " degrees F."
		
	def k2f(self, t):
		return round((t*9/5.0)-459.67)