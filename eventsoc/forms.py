from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from eventsoc.models import UserProfile, Society, Event, Category
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
        """
        check email already exists
        :return: cleaned email
        """
        email = self.cleaned_data.get('email', None)
        # Checks that the email is unique when creating account
        if self.cleaned_data.get('username') == "":
            if UserProfile.objects.filter(email=email):
                raise forms.ValidationError('That email is already registered!')
            return email
        # Checks, when the email is changed, that it is unique
        username = self.cleaned_data.get('username')
        if email and UserProfile.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('That email is already registered!')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password has to match")

        if not self.validate_password_strength():
            raise forms.ValidationError(
                'Password must contain at least 1 digit and letter.')
        return password2

    def validate_password_strength(self):
        """
        Validates that a password is at least 7 characters long and had
        at least 1 digit and 1 letter
        """
        min_length = 8
        value = self.cleaned_data['password1']

        # Check min value
        if len(value) < min_length:
            raise forms.ValidationError(
                'Password must be at least {0} characters long'.format(min_length))

        # Check if the password contains a digit
        if not any(char.isdigit() for char in value):
            raise forms.ValidationError(
                'Password must contain at least 1 digit')

        # Check if the password contain a letter
        if not any(char.isalpha() for char in value):
            raise forms.ValidationError(
                'Password must contain at least 1 letter')

        return True

    def save(self, commit=True):
        userAccount = super().save(commit=False)
        userAccount.is_user = True
        userAccount.is_active = True
        if commit:
            userAccount.save()
        return userAccount


class SocietyForm(UserCreationForm):
    logo = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2', 'email', 'logo')

    def clean_email(self):
        """
        check email already exists
        :return: cleaned email
        """
        email = self.cleaned_data.get('email', None)
        # Checks that the email is unique when creating account
        if self.cleaned_data.get('username') == "":
            if UserProfile.objects.filter(email=email):
                raise forms.ValidationError('That email is already in registered!')
            return email
        username = self.cleaned_data.get('username')
        # Checks, when the email is changed, that it is unique
        if email and UserProfile.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('That email is already in registered!')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password has to match")

        if not self.validate_password_strength():
            raise forms.ValidationError(
                'Password must contain at least 1 digit and letter.')
        return password2

    def validate_password_strength(self):
        """
        Validates that a password is at least 7 characters long and had
        at least 1 digit and 1 letter
        """
        min_length = 8
        value = self.cleaned_data['password1']

        # Check min value
        if len(value) < min_length:
            raise forms.ValidationError(
                'Password must be at least {0} characters long'.format(min_length))

        # Check if the password contains a digit
        if not any(char.isdigit() for char in value):
            raise forms.ValidationError(
                'Password must contain at least 1 digit')

        # Check if the password contain a letter
        if not any(char.isalpha() for char in value):
            raise forms.ValidationError(
                'Password must contain at least 1 letter')

        return True

    def save(self):
        user = super().save(commit=False)
        user.is_society = True
        user.is_active = True
        user.save()
        # Gets a society object if society editing it's profile or creates a society object if a society is registering
        try:
            society = Society.objects.get(user=user)
            society.email = self.cleaned_data['email']
            society.logo = self.cleaned_data['logo']
        except Society.DoesNotExist:
            society = Society.objects.create(user=user)
            society.email = self.cleaned_data['email']
            society.logo = self.cleaned_data['logo']
        return user
