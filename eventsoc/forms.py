from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from eventsoc.models import UserProfile, Society, Event, Category
from django.contrib.auth.forms import UserCreationForm
# May only need one of these event forms
# Might not want to have queryset


class EventForm(forms.ModelForm):
    title = forms.CharField(required=True)
    category = ModelChoiceField(required=True, queryset=Category.objects.all())
    date = forms.DateTimeField(required=True, help_text="Please use the format: YYYY-MM-DD")
    time = forms.TimeField(required=True, help_text='Please use the format: <em>HH:MM:SS<em')
    place_name = forms.CharField(max_length=50)
    room = forms.CharField(max_length=10)
    address = forms.CharField(max_length=50)
    price = forms.IntegerField(required=True, initial=0)
    description = forms.CharField(required=True, max_length=10000)
    capacity = forms.IntegerField(required=True, initial=0)
    picture = forms.ImageField()

    class Meta:
        model = Event
        exclude = ('creator',)
        fields = ('title', 'category', 'date', 'time', 'place_name', 'room', 'address', 'price', 'description', 'capacity', 'picture')



# Probably won't be needed, currently isn't used
class EditEventForm(forms.ModelForm):
    title = forms.CharField(required=True)
    category = ModelChoiceField(required=True, queryset=Category.objects.all())
    event_date = forms.DateTimeField(required=True, help_text="Please use the format: YYYY-MM-DD")
    time = forms.TimeField(required=True, help_text='Please use the format: <em>HH:MM:SS<em')
    place_name = forms.CharField(max_length=50)
    room = forms.CharField(max_length=10)
    address = forms.CharField(max_length=50)
    price = forms.IntegerField(required=True, initial=0)
    price = forms.IntegerField(required=True, initial=0)
    description = forms.CharField(required=True, max_length=10000)
    picture = forms.ImageField()

    class Meta:
        model = Event
        fields = ('title', 'category', 'event_date', 'time', 'place_name', 'room', 'address', 'price', 'description', 'picture')


# class EditProfile(forms.ModelForm):
    #
    # class Meta:
    #     model = UserProfile
    #     fields = ('username', 'password', 'email')


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')

    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2', 'email')

    def clean_email(self):
        """
        check email already exists
        :return: cleaned email
        """
        email = self.cleaned_data.get('email', None)
        if UserProfile.objects.filter(email=email):
            raise forms.ValidationError('That email is already in registered!')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not self.validate_password_strength():
            raise forms.ValidationError('Password must contain at least 1 digit and letter.')
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
            raise forms.ValidationError('Password must be at least {0} characters long'.format(min_length))

        # Check if the password contains a digit
        if not any(char.isdigit() for char in value):
            raise forms.ValidationError('Password must contain at least 1 digit')

        # Check if the password contain a letter
        if not any(char.isalpha() for char in value):
            raise forms.ValidationError('Password must contain at least 1 letter')

        return True

    def save(self, commit=True):
        userAccount = super().save(commit=False)
        userAccount.is_user = True
        if commit:
            userAccount.save()
        return userAccount


class SocietyForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
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
        if UserProfile.objects.filter(email=email):
            raise forms.ValidationError('That email is already in registered!')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not self.validate_password_strength():
            raise forms.ValidationError('Password must contain at least 1 digit and letter.')
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
            raise forms.ValidationError('Password must be at least {0} characters long'.format(min_length))

        # Check if the password contains a digit
        if not any(char.isdigit() for char in value):
            raise forms.ValidationError('Password must contain at least 1 digit')

        # Check if the password contain a letter
        if not any(char.isalpha() for char in value):
            raise forms.ValidationError('Password must contain at least 1 letter')

        return True

    def save(self):
        user = super().save(commit=False)
        user.is_society = True
        user.save()
        society = Society.objects.create(user=user)
        society.email = self.cleaned_data['email']
        society.logo = self.cleaned_data['logo']
        return user
