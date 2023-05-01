from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .models import Event, UsersEvents, Users
from event.forms import EventForm, UsersEventsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse


def index(request):
    template = loader.get_template('event/index.html')
    events = Event.objects.exclude(user_id=request.user.id).order_by('-name')
    user_event = Event.objects.filter(user_id=request.user.id)
    context = {'events': events, 'user_event': user_event}
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
        form = EventForm(initial={'user': request.user.id})
        if not request.user.is_superuser:
            form.fields['user'].disabled = True
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
    try:
        ues = UsersEvents.objects.filter(event_id=event_id)
    except UsersEvents.DoesNotExist:
        ues = None
    return render(request, 'event/update.html', {'form': form, 'user_events': ues})


@login_required
@transaction.atomic
def update_userevent(request, ue_id):
    user_event = UsersEvents.objects.get(pk=ue_id)
    if request.POST:
        form = UsersEventsForm(request.POST, instance=UsersEvents.objects.get(pk=ue_id))
        if form.is_valid():
            form.save(commit=False)
            form.users_id = user_event.users_id
            form.event_id = user_event.event_id
            form.save()
            event = Event.objects.get(pk=user_event.event_id)
            return redirect('by_event', event_id=event.id)
    else:
        form = UsersEventsForm(instance=user_event)
        form.date_reg = user_event.date_reg
    return render(request, 'event/updateuserevent.html', {'form': form, 'users': Users.objects.get(pk=user_event.users_id), 'ue_id': ue_id})


@login_required
@transaction.atomic
def delete_userevent(request, ue_id):
    event = UsersEvents.objects.get(pk=ue_id)
    event_id = Event.objects.get(pk=event.event_id).id
    event.delete()
    return HttpResponseRedirect(reverse('by_event', args=(event_id,)))


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
    try:
        ues = UsersEvents.objects.filter(event_id=event_id)
    except UsersEvents.DoesNotExist:
        ues = None
    context = {'events': events, 'event': current_event, 'user_events': ues}
    return render(request, 'event/event.html', context)


@login_required()
def sign_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    user = request.user
    users = Users.objects.get(user_id=user.pk)
    UsersEvents.objects.update_or_create(
        users=users,
        event=event
    )
    return HttpResponseRedirect(reverse('by_event', args=(event_id,)))

# class EventListView(ListView):
#     model = Event
#     template_name = 'event/index.html'
