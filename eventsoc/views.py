from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import permission_required, login_required
from eventsoc.forms import UserForm, SocietyForm, EditEventForm, EventForm
from eventsoc.models import Society, Event, NewUser
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    return render(request, "eventsoc/index.html", {})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                print("here")
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                print("here")
                return HttpResponse("account disabled")
        else:
            return(HttpResponse("Invalid login details"))
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


#@login_required
# @permission_required(eventsoc.is_society)


@login_required
>>>>>>> Login view and society and user forms
def create_event(request):
    # event_form = EventForm()
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save(commit = True)
            # return index(request)
        else:
            print(form.errors)
    else:
        event_form = EventForm
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
            elif user_form.is_valid() == False:
                print(user_form.errors)

        elif 'society_register' in request.POST:
            if society_form.is_valid():
                society = society_form.save()
                society.set_password(society.password)
                society.save()
                registered = True
            elif society_form.is_valid == False:
                print(society_form.errors)
    else:
        user_form = UserForm()
        society_form = SocietyForm()
    return render(request, 'eventsoc/register.html',
                {'user_form': user_form,
                'society_form': society_form,
                'registered': registered})

@login_required
def edit_event(request):
    # society = NewUser.objects.get(id=request.user.id)
    # event_form = EventForm()
    # form = EditEventForm(instance=event_form)
    if request.user.is_authenticated:
        society = request.user
    else:
        return(HttpResponse("Not logged in"))

    # Seems to allways return false
    print(society.is_society)

    if request.user.is_authenticated: #and society.is_society:
        if request.method == 'POST':
            # form = EditEventForm(request.POST, instance=event_form)
            form = EditEventForm(request.POST)
            if form.is_valid:
                update = form.save()
                update.society = society
                update.save()
            return render(request, 'wad_project/edit_event', {'event_form': form})
        else:
            return(HttpResponse("No input"))
    else:
        return(HttpResponse("Not a society"))


# @login_required
def edit_profile(request):
    user = NewUser.objects.get(id=request.user.id)
    user_form = user.event
    form = UserForm(instance=user_form)

    if request.user.is_authenticated() and request.user.is_user:
        if request.method == 'POST':
            form = UserForm(request.POST, instance=user_form)

            if form.is_valid:
                update = form.save()
                update.user = user
                update.save()
            return render(request, 'wad_project/edit_profile', {})
    else:
        form = UserForm(instance=user_form)
    # return render(request, "eventsoc/edit_profile.html", {})


#@login_required
def booked(request):
    return render(request, "eventsoc/booked.html", {})


@login_required
def account(request):
    return render(request, "eventsoc/account.html", {})


def society(request):
    return render(request, "eventsoc/society.html", {})


@login_required
def past_events(request):
    return render(request, "eventsoc/past_events.html", {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
