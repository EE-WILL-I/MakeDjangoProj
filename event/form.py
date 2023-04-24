from django.forms import ModelForm
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('desctiption', 'title', 'type', 'logo', 'data_event', 'duration', 'city')