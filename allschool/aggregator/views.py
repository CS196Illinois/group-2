from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout


# Create your views here.
def index(request):
    return HttpResponse("Temp: Index")

def home(request):
    return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return render(request, 'home.html')