from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, "eventsoc/index.html", {})


def login(request):
    return render(request, "eventsoc/login.html", {})


def create_event(request):
    return render(request, "eventsoc/create_event.html", {})


def register(request):
    return render(request, "eventsoc/register.html", {})


def edit_event(request):
    return render(request, "eventsoc/edit_event.html", {})


def edit_profile(request):
    return render(request, "eventsoc/edit_profile.html", {})


def booked(request):
    return render(request, "eventsoc/booked.html", {})


def account(request):
    return render(request, "eventsoc/account.html", {})


def society(request):
    return render(request, "eventsoc/society.html", {})


def past_events(request):
    return render(request, "eventsoc/past_events.html", {})


def user_logout(request):
    return render(request, "eventsoc/user_logout.html", {})
