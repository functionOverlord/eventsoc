from django.contrib.auth.models import User
from eventsoc.models import UserProfile, Society, Event, Category
import django.contrib.auth.password_validation as validators
from django import forms

# Common functions that the forms use

# Verifies email
def check_email(self):
    """
    check email already exists
    :return: cleaned email
    """

    email = self.cleaned_data.get('email', None)
    user = UserProfile.objects.filter(email=email).values('username')
    uservalues = user.values()
    username = self.cleaned_data.get('username')
    
    # Checks that the email is unique when creating account
    if username not in user and username != None:
        if UserProfile.objects.filter(email=email):
            raise forms.ValidationError('That email is already registered!')
        return email

    # Checks, when the email is changed, that it is unique
    if uservalues.first() != None:
        if email and UserProfile.objects.filter(email=email).exclude(username=uservalues.first()['username']).count():
            raise forms.ValidationError('That email is already registered!')
    return email


# Verifies password
def check_password(self):
    """
    Check password's strength
    :return: cleaned password
    """
    password1 = self.cleaned_data.get('password1')
    try:
        validators.validate_password(password1, self.instance)
    except forms.ValidationError as error:
        # Method inherited from BaseForm
        self.add_error('password1', error)
    return password1
