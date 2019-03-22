from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from eventsoc.forms import StudentForm, SocietyForm, EditEventForm, EventForm, EditSocietyForm, EditStudentForm
from eventsoc.models import Society, Event, UserProfile, Category, Booking, Bookmark
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.db.models import F


def index(request):
    trending_events = Event.objects.order_by(
        '-popularity')[:5]  # TODO correct sorting order?
    upcoming_events = Event.objects.order_by('date')
    return render(request,
                  "eventsoc/index.html",
                  {'trending_events': trending_events,
                   'upcoming_events': upcoming_events})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                # We'll send the user back to the homepage
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your EventSoc account is disabled!")
        else:
            # Bad login details were provided. So we can't log the user in.
            messages.add_message(
                request,
                messages.ERROR,
                "Incorrect user or password")
            return HttpResponseRedirect(reverse('login'))
    # The request is not a HTTP POST, so display the login form.
    else:
        return render(request, 'eventsoc/login.html', {})


def show_event(request, slug):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(id=request.user.id)
        event = Event.objects.get(slug=slug)
        booked = Booking.objects.filter(user=user, event=event).exists()
        bookmarked = Bookmark.objects.filter(user=user, event=event).exists()
        creator = False
        if event.creator == user:
            creator = True
        return render(request, 'eventsoc/event.html',
                      {'slug': slug, 'event': event, 'creator': creator, 'booked': booked, 'bookmarked': bookmarked})
    else:
        event = Event.objects.get(slug=slug)
        return render(request, 'eventsoc/event.html',
                      {'slug': slug, 'event': event})

@user_passes_test(lambda u: u.is_society, login_url='index')
def create_event(request):
    event_form = EventForm()
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save(commit=True)
            event.creator = request.user
            event.save()
            # Redirect user to the event page they've created
            return redirect('../event/'+event.slug)
        else:
            print(event_form.errors)

    return render(request, 'eventsoc/create_event.html',
                  {'event_form': event_form})


def register(request):
    # A boolean value for telling the template whether the registration was successful
    registered = False

    # If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        # Attempt to grab information from raw form information
        user_form = StudentForm(data=request.POST)
        society_form = SocietyForm(data=request.POST)

        # If it's a student:
        if 'user_register' in request.POST:
            if user_form.is_valid():
                user = user_form.save()
                user.save()
                registered = True
                login(request, user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Successfully registered!")
                return redirect('index')
            else:
                print(user_form.errors)

        # If it's a society:
        elif 'society_register' in request.POST:
            if society_form.is_valid():
                society = society_form.save()

                 # Sorting out the society logo
                if 'logo' in request.FILES:
                    society.logo = request.FILES['logo']

                society.save()
                registered = True
                login(request, society)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Successfully registered!")
                return redirect('index')
            else:
                print(society_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
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
        if event.creator == request.user:
            if request.method == 'POST':
                event_form = EventForm(request.POST, request.FILES, instance=event)
                if event_form.is_valid:
                    update = event_form.save()
                    update.society = society
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "Successfully saved!")
                    update.save()
            else:
                events = []
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Cannot edit this event as it does not belong to you!")
    else:
        events = []
    return render(request, 'eventsoc/edit_event.html',
                  {'event_form': event_form, 'event': event, 'slug': slug})


@user_passes_test(lambda u: u.is_society, login_url='index')
def delete_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    creator = request.user
    errormsg=''
    if request.method == 'GET':
        if event.creator == creator:
            event.delete()
            return redirect('/')
    return render(request, 'eventsoc/delete_event.html', {"event": event})


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering
    # engine
    context_dict = {}

    try:
        # Find category name slug with the given name
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all associated events.
        # filter() will return a list of event object or an empty list.
        upcoming_events = Event.objects.filter(
            category=category).order_by('date')

        # Retrieve popular events in the category
        trending_events = Event.objects.filter(category=category).order_by(
            '-popularity')[:5]  # TODO correct sorting order?

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


@login_required
def edit_profile(request):
    user = UserProfile.objects.get(id=request.user.id)
    if request.user.is_authenticated and request.user.is_user:
        form = EditStudentForm(instance=user)
    else:
        form = EditSocietyForm(instance=user)

    if request.user.is_authenticated and request.user.is_user:
        if request.method == 'POST':
            form = EditStudentForm(request.POST, instance=user)
            if form.is_valid():
                update = form.save()
                update.user = user
                form.save()
                # new_user = authenticate(creator=form.creator, password=form.password)
                update_session_auth_hash(request, user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Successfully saved!")
                login(request, user)
    elif request.user.is_authenticated and request.user.is_society:
        if request.method == 'POST':
            form = EditSocietyForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                update = form.save()
                # Logo edit can cause errors if used multiple times
                newlogo = UserProfile(logo = request.FILES['logo'])
                newlogo.save()
                update.user = user
                form.save()
                # new_user = authenticate(creator=form.creator, password=form.password)
                update_session_auth_hash(request, user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Successfully saved!")
                login(request, user)
    else:
        form = EditStudentForm(instance=user)
    return render(request, 'eventsoc/edit_profile.html', {'form': form})


# These views need to order the events by date

# Returns the events that the user has booked
@user_passes_test(lambda u: u.is_user, login_url='index')
def booked(request):
    booked_events = Booking.objects.filter(user=request.user)
    temp=[]
    counter = 0
    for i in booked_events:
        booking = booked_events.values('event_id')[counter]
        temp.append(Event.objects.get(id=booking['event_id']))
        counter+=1
    return render(request, 'eventsoc/booked.html',{'books':temp})

# Returns the events that the user has bookmarked
@user_passes_test(lambda u: u.is_user, login_url='index')
def bookmarked(request):
    bookmarked_events = Bookmark.objects.filter(user=request.user)
    temp=[]
    counter = 0
    for i in bookmarked_events:
        booking = bookmarked_events.values('event_id')[counter]
        temp.append(Event.objects.get(id=booking['event_id']))
        counter+=1
    print(temp)
    return render(request, "eventsoc/bookmarked.html",
                  {'upcoming_events': temp})


@login_required
def account(request):
    user = UserProfile.objects.get(id=request.user.id)
    if user.is_society:
        events = Event.objects.filter(creator=user)
        return render(request, "eventsoc/account.html",
                      {'user': user, 'events': events})
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
    return render(request, "eventsoc/past_events.html",
                  {'upcoming_events': upcoming_events})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



# Increments event.booked and creates a booking for each user
@login_required
def booking(request, slug):
    if request.method == 'GET':
        event = get_object_or_404(Event, slug=slug)
        event.bookings =  F('bookings') + 1
        event.save()
        booking = Booking(user=request.user, event=event, booked=True)
        booking.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Successfully booked!")
    return redirect('../')

# Decrements event.booked and deletes a user's booking
@login_required
def cancel_booking(request, slug):
    if request.method == 'GET':
        event = get_object_or_404(Event, slug=slug)
        event.bookings =  F('bookings') - 1
        event.save()
        booking = Booking.objects.get(user=request.user, event=event, booked=True)
        booking.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Successfully cancelled booking!")
    return redirect('../')

# Bookmarks an event for a user
@login_required
def bookmark(request, slug):
    if request.method == 'GET':
        event = get_object_or_404(Event, slug=slug)
        bookmark = Bookmark(user=request.user, event=event, bookmarked=True)
        bookmark.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Successfully bookmarked!")
    return redirect('../')

# Removes a bookmark for a user
@login_required
def remove_bookmark(request, slug):
    if request.method == 'GET':
        event = get_object_or_404(Event, slug=slug)
        bookmark = Bookmark.objects.get(user=request.user, event=event, bookmarked=True)
        print(bookmark)
        bookmark.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Successfully removed bookmark!")
    return redirect('../')
