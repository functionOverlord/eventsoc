from django import forms
from django.contrib.auth.models import User
from eventsoc.models import UserProfile, Society, Event, Category
from django.contrib.auth.forms import UserCreationForm
from eventsoc.form_functions import check_email, check_password


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('creator', 'slug', 'popularity', 'bookings')


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
    society_name = forms.CharField(max_length=200, required=True)
    social_media_website = forms.URLField()

    class Meta:
        model = UserProfile
        fields = ('username', 'society_name', 'social_media_website', 'password1', 'password2', 'email', 'logo')

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
        society.social_media_website = self.cleaned_data['social_media_website']
        society.society_name = self.cleaned_data['society_name']
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
        fields = ('society_name', 'social_media_website', 'password1', 'password2', 'email', 'logo')
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
        society.social_media_website = self.cleaned_data['social_media_website']
        society.society_name = self.cleaned_data['society_name']
        society.email = self.cleaned_data['email']
        society.logo = self.cleaned_data['logo']
        return user
