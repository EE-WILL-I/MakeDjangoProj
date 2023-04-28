from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Event

def index(request):
    template = loader.get_template('event/index.html')
    Event.objects.all()
    events = Event.objects.order_by('-name')
    context = {'events': events}
    return HttpResponse(template.render(context, request))


def by_event(request, event_id):
    bbs = Event.objects.all()
    current_event = Event.objects.get(pk=event_id)
    context = {'bbs': bbs, 'current_event': current_event}
    return render(request, 'event/event.html', context)

# class EventListView(ListView):
#     model = Event
#     template_name = 'event/index.html'
