from django.db import models
from django.contrib.auth.models import User
import datetime
import json
import requests


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)
	
class City(models.Model):
	api_id = models.IntegerField()
	name = models.CharField(max_length=100)
	subscribers = models.ManyToManyField(User)
	cached = models.CharField(max_length=1000,default="")
	modified_date = models.DateTimeField(auto_now=True)
	
	def get_details(self):
		if(datetime.datetime.now() - self.modified_date > 10 * 60):
			cached = self.pull_from_api()
		result = json.loads(cached)
		return result
		
	def pull_from_api(self):
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?id=" + self.api_id + "&appid=cdfdac6c8b96346016dea9fa93d524b6")
		return r.body