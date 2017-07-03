import requests
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import Greeting
from .models import City

# Create your views here.
def hello_index(request):
    times = int(os.environ.get('TIMES',3))
    return HttpResponse('Hello! ' * times)

def index_teapot(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')

def index(request):
    context = {}
    if request.user.is_authenticated():
        context["cities"] = City.objects.filter(subscribers__id=request.user.id) #request.user.cities
    else:
        context["cities"] = [City.objects.get(api_id=4254010)]
    for city in context["cities"]:
        city.get_details()
    return render(request, 'index.html', context)

def cities(request):
    context = {}
    context["cities"] = City.objects.filter(subscribers__id=request.user.id)
    context["other_cities"] = City.objects.exclude(subscribers__id=request.user.id)
    return render(request, 'cities.html', context)

def subscribe(request, id):
	city = City.objects.get(api_id=int(id))
	city.subscribers.add(request.user)
	city.save()
	return redirect('/cities')
	
def unsubscribe(request, id):
	city = City.objects.get(api_id=int(id))
	city.subscribers.remove(request.user)
	city.save()
	return redirect('/cities')
	
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

