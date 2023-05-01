from django import forms
from django.contrib.auth.models import User
from django.forms import models

from .models import Event, Users, UsersEvents, Status
from datetime import datetime


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
        fields = ('__all__')
        widgets = {
            'data_start': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
            'data_end': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            )
        }


class UsersEventsForm(forms.ModelForm):
    class Meta:
        model = UsersEvents
        fields = ('link_certificate', 'rating', 'status')
