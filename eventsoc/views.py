from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def login(request):
    return HttpResponse("Login")

def create_event(request):
    return HttpResponse("Create events page")

def register(request):
    return HttpResponse("register")

def edit_event(request):
    return HttpResponse("edit_event")

def edit_profile(request):
    return HttpResponse("edit_profile")

def booked(request):
    return HttpResponse("booked")

def account(request):
    return HttpResponse("account")

def society(request):
    return HttpResponse("society")

def past_events(request):
    return HttpResponse("past_events")

def user_logout(request):
    return HttpResponse("user_logout")
