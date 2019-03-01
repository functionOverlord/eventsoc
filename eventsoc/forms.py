from django import forms
from django.contrib.auth.models import User
from eventsoc.models import UserProfile, Society, Event

class EditEventForm(forms.ModelForm):
    title = forms.CharField(required=True)
    event_date = forms.DateTimeField(required=True, help_text="Please use the format: YYYY-MM-DD")
    time = forms.TimeField(required = True, help_text='Please use the format: <em>HH:MM:SS<em')
    # place = forms.ForeignKey(Place, required=True)
    price = forms.IntegerField(required=True, initial=0)
    description = forms.CharField(required=True, max_length=10000)
    # picture = forms.ImageField(upload_to='events')

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
