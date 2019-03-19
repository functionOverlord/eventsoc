from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from eventsoc.forms import StudentForm, SocietyForm, EditEventForm, EventForm
from eventsoc.models import Society, Event, UserProfile, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import DeleteView


def index(request):
    trending_events = Event.objects.order_by('-popularity')[:5]  # TODO correct sorting order?
    upcoming_events = Event.objects.order_by('date')
    return render(request, "eventsoc/index.html", {'trending_events': trending_events,
                                                   'upcoming_events': upcoming_events})


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
            messages.add_message(request, messages.ERROR, "Incorrect user or password")
            return HttpResponseRedirect(reverse( 'login' ))
            #return HttpResponse("Invalid login details")
            #print("Invalid login details:{0}, {1}".format(username, password))
    else:
        return render(request, 'eventsoc/login.html', {})


def event(request, slug):
    event = Event.objects.get(slug=slug)
    return render(request, 'eventsoc/event.html', {'slug': slug, 'event': event})


@user_passes_test(lambda u: u.is_society, login_url='index')
def create_event(request):
    event_form = EventForm()
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save(commit=True)
            event.creator = request.user
            event.save()
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
        user_form = StudentForm(data=request.POST)
        society_form = SocietyForm(data=request.POST)
        if 'user_register' in request.POST:
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                registered = True
                login(request, user)
            else:
                print(user_form.errors)

        elif 'society_register' in request.POST:
            if society_form.is_valid():
                society = society_form.save()
                society.set_password(society.password)
                society.save()
                registered = True
                login(request, society)
            else:
                print(society_form.errors)
    else:
        user_form = StudentForm()
        society_form = SocietyForm()
    return render(request, 'eventsoc/register.html',
                  {'user_form': user_form,
                   'society_form': society_form,
                   'registered': registered})


@user_passes_test(lambda u: u.is_society, login_url='index')
def edit_event(request, slug):
    society = UserProfile.objects.get(id=request.user.id)
    event = Event.objects.get(slug=slug)
    event_form = EventForm(instance=event)
    if request.user.is_authenticated:
        if request.method == 'POST':
            event_form = EventForm(request.POST, request.FILES, instance=event)
            if event_form.is_valid:
                update = event_form.save()
                update.society = society
                update.save()
        else:
            events = []
    else:
        events = []
    return render(request, 'eventsoc/edit_event.html', {'event_form': event_form, 'event': event, 'slug': slug})


@user_passes_test(lambda u: u.is_society, login_url='index')
def delete_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    creator = request.user
    if request.method == 'GET':
        if event.creator == creator:
            event.delete()
            return redirect('/')

    return render(request, 'eventsoc/delete_event.html', {"event": event})


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine
    context_dict = {}

    try:
        # Find category name slug with the given name
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all associated events.
        # filter() will return a list of event object or an empty list.
        upcoming_events = Event.objects.filter(category=category).order_by('date')

        # Retrieve popular events in the category
        trending_events = Event.objects.filter(category=category).order_by('-popularity')[:5]  # TODO correct sorting order?

        context_dict['trending_events'] = trending_events
        context_dict['upcoming_events'] = upcoming_events

        # Also add the category object from the database to the context_dictionary
        # Use this in the template to verify that the category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        # Got here if we didn't find the specified category
        context_dict['category'] = None
        context_dict['upcoming_events'] = None

    # Go render the response and return it to the client
    return render(request, "eventsoc/index.html", context_dict)


# @login_required
@user_passes_test(lambda u: u.is_user, login_url='index')
def edit_profile(request):
    user = UserProfile.objects.get(id=request.user.id)
    form = StudentForm(instance=user)
    if request.user.is_authenticated and request.user.is_user:
        if request.method == 'POST':
            form = StudentForm(request.POST, instance=user)

            if form.is_valid:
                update = form.save()
                update.user = user
                form.save()
                # new_user = authenticate(username=form.username, password=form.password)
                update_session_auth_hash(request, user)
                login(request, user)
    else:
        form = StudentForm(instance=user)
    return render(request, 'eventsoc/edit_profile.html', {'form': form})


@user_passes_test(lambda u: u.is_user, login_url='index')
def booked(request):
    upcoming_events = Event.objects.order_by('date')
    return render(request, "eventsoc/booked.html", {'upcoming_events': upcoming_events})


@login_required
def account(request):
    user = UserProfile.objects.get(id=request.user.id)
    if user.is_society:
        # Need to pass the society's logo
        events = Event.objects.filter(creator=user)
        return render(request, "eventsoc/account.html", {'user': user, 'events': events})
    else:
        return render(request, "eventsoc/account.html", {'user': user})


@user_passes_test(lambda u: u.is_society, login_url='index')
def society(request):
    society = UserProfile.objects.get(id=request.user.id)
    form = SocietyForm(instance=society)
    return render(request, "eventsoc/society.html", {'form': form})


# @login_required
def past_events(request):
    upcoming_events = Event.objects.order_by('date')
    return render(request, "eventsoc/past_events.html", {'upcoming_events': upcoming_events})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
