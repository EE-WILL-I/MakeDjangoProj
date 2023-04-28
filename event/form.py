from django import forms
from django.contrib.auth.models import User
from .models import Event, Users
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('second_name', 'age', 'city', 'sex')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'desctiption', 'logo', 'status_event', 'data_start', 'data_end', 'city')



