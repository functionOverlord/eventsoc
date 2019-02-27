from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def create_event(request):
    return HttpResponse("Create events page")

def login(request):
    return HttpResponse("Login")
