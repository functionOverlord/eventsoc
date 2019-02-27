from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required

# Permissions will be defined in models

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def login(request):
    return HttpResponse("Login")

@login_required
@permission_required(eventsoc.is_society)
def create_event(request):
    return HttpResponse("Create events page")

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        society_form = SocietyForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        elif user_form.is_valid() == False:
            print(user_form.errors)

        if society_form.is_valid:
            society = society_form.save()
            society.set_password(society.password)
            society.save()
            registered = True
        elif society_form.is_valid == False:
            print(society_form.errors)
    else:
        user_form = UserForm()
        society_form = SocietyForm()
    return render(request, 'wad_project/register.html',
                {'user_form': user_form,
                'society_form': society_form,
                'registered': registered})

@login_required
@permission_required(eventsoc.is_society)
def edit_event(request):
    return HttpResponse("edit_event")

@login_required
def edit_profile(request):
    return HttpResponse("edit_profile")

@login_required
@permission_required(eventsoc.is_user)
def booked(request):
    return HttpResponse("booked")

@login_required
@permission_required(eventsoc.is_user)
def account(request):
    return HttpResponse("account")

def society(request):
    return HttpResponse("society")

@login_required
@permission_required(eventsoc.society)
def past_events(request):
    return HttpResponse("past_events")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
