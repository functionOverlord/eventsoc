from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from eventsoc.forms import UserForm, SocietyForm, EditEventForm, EventForm
from eventsoc.models import Society, Event, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import redirect


# Create your views here.


def index(request):
    # Possibly swap capacity for popularity
    event_list = Event.objects.order_by('-capacity')[:3]
    return render(request, "eventsoc/index.html", {'event_list': event_list})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("account disabled")
        else:
            return (HttpResponse("Invalid login details"))
            print("Invalid login details:{0}, {1}".format(username, password))

        soc_username = request.POST.get('username')
        soc_password = request.POST.get('password')
        society = authenticate(username=soc_username, password=soc_password)
        if society:
            if society.is_active:
                login(request, society)
                return HttpResponseRedirect(reverse('eventsoc/index.html'))
            else:
                return HttpResponse("Invalid login details")
        else:
            print("Invalid login details:{0}, {1}".format(username, password))
    else:
        return render(request, 'eventsoc/login.html', {})


def event(request):
    return render(request, 'event')


@user_passes_test(lambda u: u.is_society, login_url='index')
def create_event(request):
    event_form = EventForm()
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event_form.save(commit=True)
            # Need to create a slug event url to direct user to the event page they've created
            # redirect = 'eventsoc/'
            # return index(request)
            return redirect('/')
        else:
            print(event_form.errors)
    return render(request, 'eventsoc/create_event.html', {'event_form': event_form})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        society_form = SocietyForm(data=request.POST)
        if 'user_register' in request.POST:
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                registered = True
                login(request, user)
            elif not user_form.is_valid():
                print(user_form.errors)

        elif 'society_register' in request.POST:
            if society_form.is_valid():
                society = society_form.save()
                society.set_password(society.password)
                society.save()
                registered = True
                login(request, society)
            elif not society_form.is_valid:
                print(society_form.errors)
    else:
        user_form = UserForm()
        society_form = SocietyForm()
    return render(request, 'eventsoc/register.html',
                  {'user_form': user_form,
                   'society_form': society_form,
                   'registered': registered})


# @login_required
# @permission_required(eventsoc.is_society)
# User needs to select an event
@user_passes_test(lambda u: u.is_society, login_url='index')
def edit_event(request):
    # society = User.objects.get(id=request.user.id)
    # event_form = EventForm()
    # form = EditEventForm(instance=event_form)
    # if request.user.is_authenticated:
    #     society = request.user
    # else:
    #     return(HttpResponse("Not logged in"))

    if request.user.is_authenticated:  # and society.is_society:
        # request.method returns get all the time
        if request.method == 'POST':
            society = request.user
            events = Event.objects.get(creator=society.creator)
            # instance should be an event
            # form = EditEventForm(request.POST, instance=event_form)
            event_form = EventForm(request.POST)
            if form.is_valid:
                update = form.save()
                update.society = society
                update.save()
        else:
            return HttpResponse("No input, request method = " + request.method)
    else:
        return HttpResponse("Not a society")
    return render(request, 'eventsoc/edit_event.html', {'event_form': event_form, 'events': events})


# @login_required
@user_passes_test(lambda u: u.is_user, login_url='index')
def edit_profile(request):
    user = UserProfile.objects.get(id=request.user.id)
    # user_form = user.event
    form = UserForm(instance=user)

    if request.user.is_authenticated and request.user.is_user:
        if request.method == 'POST':
            form = UserForm(request.POST, instance=user)

            if form.is_valid:
                update = form.save()
                update.user = user
                form.save()
                # new_user = authenticate(username=form.username, password=form.password)
                update_session_auth_hash(request, user)
                login(request, user)
    else:
        form = UserForm(instance=user)
    return render(request, 'eventsoc/edit_profile.html', {'form': form})


# @login_required
def booked(request):
    return render(request, "eventsoc/booked.html", {})


# @login_required
# @user_passes_test(lambda u: u.is_user, login_url='index')
def account(request):
    user = UserProfile.objects.get(id=request.user.id)
    if user.is_society:
        account_form = SocietyForm(instance=society)
        return render(request, "eventsoc/account.html", {'account_form': account_form})
    else:
        account_form = UserForm(instance=user)
        return render(request, "eventsoc/account.html", {'account_form': account_form})


@user_passes_test(lambda u: u.is_society, login_url='index')
def society(request):
    society = UserProfile.objects.get(id=request.user.id)
    form = SocietyForm(instance=society)
    return render(request, "eventsoc/society.html", {'form': form})


# @login_required
def past_events(request):
    return render(request, "eventsoc/past_events.html", {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
