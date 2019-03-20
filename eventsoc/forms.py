from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from eventsoc.models import UserProfile, Society, Event, Category
from django.contrib.auth.forms import UserCreationForm
import django.contrib.auth.password_validation as validators
# May only need one of these event forms
# Might not want to have queryset


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('creator', 'slug', 'popularity')


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

    def clean_password(self):
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

    def clean_email(self):
        """
        Check email already exists
        :return: cleaned email
        """
        email = self.cleaned_data.get('email', None)
        if UserProfile.objects.filter(email=email):
            raise forms.ValidationError('That email is already in registered!')
        return email

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

    def clean_password(self):
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

    def clean_email(self):
        """
        Check email already exists
        :return: cleaned email
        """
        email = self.cleaned_data.get('email', None)
        if UserProfile.objects.filter(email=email):
            raise forms.ValidationError('That email is already in registered!')
        return email

    def save(self):
        user = super().save(commit=False)
        user.is_active = True
        user.is_society = True
        user.save()
        society = Society.objects.create(user=user)
        society.social_media_website = self.cleaned_data['social_media_website']
        society.email = self.cleaned_data['society_name']
        society.email = self.cleaned_data['email']
        society.logo = self.cleaned_data.get('logo')
        return user
