from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from event.models import Users


class SignupForm1(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Email user')
    first_name = forms.CharField(max_length=200, help_text='Name user')
    last_name = forms.CharField(max_length=200, help_text='Family user')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class SignupForm2(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('second_name', 'age', 'city', 'sex')