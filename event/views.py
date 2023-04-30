from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .models import Event
from event.forms import EventForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse


def index(request):
    template = loader.get_template('event/index.html')
    Event.objects.all()
    events = Event.objects.order_by('-name')
    context = {'events': events}
    return HttpResponse(template.render(context, request))


@login_required
@transaction.atomic
def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('by_event', event_id=event.pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EventForm()
    return render(request, 'event/newevent.html', {'form': form})


@login_required
@transaction.atomic
def update_event(request, event_id):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=Event.objects.get(pk=event_id))
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('by_event', event_id=event.pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EventForm(instance=Event.objects.get(pk=event_id))
    return render(request, 'event/update.html', {'form': form})


@login_required
@transaction.atomic
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return HttpResponseRedirect(reverse('index'))


@login_required
def by_event(request, event_id):
    events = Event.objects.all()
    current_event = Event.objects.get(pk=event_id)
    context = {'events': events, 'event': current_event}
    return render(request, 'event/event.html', context)


@login_required()
def sign_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    context = {'event': event}
    return render(request, 'event/event.html', context)

# class EventListView(ListView):
#     model = Event
#     template_name = 'event/index.html'
