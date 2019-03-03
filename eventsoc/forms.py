from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from eventsoc.models import UserProfile, Society, Event, Category, Place

# May only need one of these event forms
# Might not want to have queryset

class EventForm(forms.ModelForm):
    title = forms.CharField(required=True)
    category = ModelChoiceField(required=True, queryset=Category.objects.all())
    event_date = forms.DateTimeField(required=True, help_text="Please use the format: YYYY-MM-DD")
    time = forms.TimeField(required = True, help_text='Please use the format: <em>HH:MM:SS<em')
    place = forms.ModelChoiceField(required = True, queryset=Place.objects.all())
    price = forms.IntegerField(required=True, initial=0)
    description = forms.CharField(required=True, max_length=10000)
    picture = forms.ImageField()

    class Meta:
        model = Event
        fields = ('title', 'category', 'event_date', 'time', 'place', 'price', 'description', 'picture')

class EditEventForm(forms.ModelForm):
    title = forms.CharField(required=True)
    category = ModelChoiceField(required=True, queryset=Category.objects.all())
    event_date = forms.DateTimeField(required=True, help_text="Please use the format: YYYY-MM-DD")
    time = forms.TimeField(required = True, help_text='Please use the format: <em>HH:MM:SS<em')
    place = forms.ModelChoiceField(required = True, queryset=Place.objects.all())
    price = forms.IntegerField(required=True, initial=0)
    description = forms.CharField(required=True, max_length=10000)
    picture = forms.ImageField()

    class Meta:
        model = Event
        fields = ('title', 'event_date', 'time', 'price', 'description', 'picture')

# class EditProfile(forms.ModelForm):
    #
    # class Meta:
    #     model = UserProfile
    #     fields = ('username', 'password', 'email')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class SocietyForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = Society
        fields = ('name', 'password', 'email', 'logo')
