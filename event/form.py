from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Event, Users


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = ('second_name', 'age', 'city', 'sex')


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'desctiption', 'logo', 'status_event', 'data_start', 'data_end', 'city')