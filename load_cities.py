#!/usr/bin/env python

import os
import json
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")
import django
django.setup()
from hello.models import City

if __name__ == '__main__':    
	City.objects.all().delete() # TODO remove this
	large_cities = {}
	with open('largest_cities.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			large_cities[row["city"]] = True
			
			
	json_data=open("city.list.json", encoding="utf8").read()
	data = json.loads(json_data)
	for city in data:
		if(city["country"] == "US" and city["name"] in large_cities):
			print(city["name"].encode("utf8"))
			attribs = {"api_id": city["id"], "name": city["name"], "weather": "Unknown", "temperature":304}
			City.objects.update_or_create(api_id=city["id"], defaults=attribs)
