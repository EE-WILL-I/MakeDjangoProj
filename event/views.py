from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.template import loader
from .models import Event, UsersEvents, Users
from event.forms import EventForm, UsersEventsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse
import os
from django.conf import settings


def index(request):
    template = loader.get_template('event/index.html')
    if request.user.is_authenticated:
        events = Event.objects.exclude(user_id=request.user.id).order_by('-name')
        user_event = Event.objects.filter(user_id=request.user.id)
        try:
            user_id = Users.objects.get(user_id=request.user.id)
            ues = UsersEvents.objects.filter(users_id=user_id)
            ues1 = []
            for ue in ues:
                ues1 += Event.objects.filter(pk=ue.event_id)
        except UsersEvents.DoesNotExist:
            ues1 = []
        except Users.DoesNotExist:
            ues1 = []
    else:
        events = Event.objects.all().order_by('-name')
        ues1 = []
        user_event = []
    context = {'events': events, 'user_event': user_event, 'ues': ues1}
    return HttpResponse(template.render(context, request))


@login_required
@transaction.atomic
def new_event(request):
    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({'user': request.user})
        form = EventForm(updated_request, request.FILES)
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
        event = Event.objects.get(pk=event_id)
        form = EventForm(instance=event, initial={'data_start': event.data_start, 'data_end': event.data_end})
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
        form = UsersEventsForm(request.POST, request.FILES, instance=UsersEvents.objects.get(pk=ue_id))
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
def delete_userevent_pk(request, ue_id):
    event = UsersEvents.objects.get(pk=ue_id)
    event_id = Event.objects.get(pk=event.event_id).id
    event.delete()
    return HttpResponseRedirect(reverse('by_event', args=(event_id,)))


@login_required
@transaction.atomic
def delete_userevent(request, event_id, user_id):
    ue_id = UsersEvents.objects.get(users_id=Users.objects.get(user_id=user_id), event_id=event_id).id
    event = UsersEvents.objects.get(pk=ue_id)
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
        user_events = UsersEvents.objects.filter(event_id=event_id)
    except UsersEvents.DoesNotExist:
        user_events = None
    try:
        user_id = Users.objects.get(user_id=request.user.id)
        ues = UsersEvents.objects.filter(users_id=user_id)
        ue1 = UsersEvents.objects.get(users_id=user_id, event_id=event_id)
        ues1 = []
        for ue in ues:
            ues1 += Event.objects.filter(pk=ue.event_id)
    except UsersEvents.DoesNotExist:
        ues1 = []
        ue1 = []
    except Users.DoesNotExist:
        ues1 = []
        ue1 = []
    context = {'events': events, 'event': current_event, 'user_events': user_events, 'ues': ues1, 'ue': ue1}
    return render(request, 'event/event.html', context)


@login_required()
@transaction.atomic
def sign_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    user = request.user
    users = Users.objects.get(user_id=user.pk)
    UsersEvents.objects.update_or_create(
        users=users,
        event=event
    )
    return HttpResponseRedirect(reverse('by_event', args=(event_id,)))


@login_required()
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
