from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from event.models import Users


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('second_name', 'age', 'city', 'sex')
