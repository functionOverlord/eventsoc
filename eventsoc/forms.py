from django import forms
from django.contrib.auth.models import User
from eventsoc.models import UserProfile, Society

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'email')

class SocietyForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = Society
        fields = ('name', 'password', 'email', 'logo')
