from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from eventsoc.models import UserProfile, Society, Event, Category
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from eventsoc.form_functions import check_email, check_password
# May only need one of these event forms
# Might not want to have queryset


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('creator', 'slug', 'popularity', 'bookings')


# Probably won't be needed, currently isn't used
class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('creator', 'slug', 'popularity')


# class EditProfile(forms.ModelForm):
    #
    # class Meta:
    #     model = UserProfile
    #     fields = ('username', 'password', 'email')


class StudentForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2', 'email')


    def clean_email(self):
        return(check_email(self))

    def clean_password(self):
        return(check_password(self))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_user = True
        user.is_active = True
        if commit:
            user.save()
        return user


class SocietyForm(UserCreationForm):
    logo = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2', 'email', 'logo')


    def clean_email(self):
        return(check_email(self))

    def clean_password(self):
        return(check_password(self))

    def save(self):
        user = super().save(commit=False)
        user.is_active = True
        user.is_society = True
        user.save()
        society = Society.objects.create(user=user)
        society.email = self.cleaned_data['email']
        society.logo = self.cleaned_data['logo']
        return user

class EditStudentForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('password1', 'password2', 'email')
        exclude = ('username', )

    def clean_email(self):
        return(check_email(self))

    def clean_password(self):
        return(check_password(self))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_user = True
        user.is_active = True
        if commit:
            user.save()
        return user

class EditSocietyForm(UserCreationForm):
    logo = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('password1', 'password2', 'email', 'logo')
        exclude = ('username', )


    def clean_email(self):
        return(check_email(self))

    def clean_password(self):
        return(check_password(self))

    def save(self):
        user = super().save(commit=False)
        user.is_active = True
        user.is_society = True
        user.save()
        society = Society.objects.get(user=user)
        society.email = self.cleaned_data['email']
        society.logo = self.cleaned_data['logo']
        return user
