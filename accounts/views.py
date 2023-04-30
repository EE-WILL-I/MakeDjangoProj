from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from accounts.forms import UserForm, UsersForm
from event.forms import UserForm, UsersForm
from django.contrib.auth.forms import UserCreationForm


@login_required
@transaction.atomic
def update_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        users_form = UsersForm(request.POST, instance=request.user.users)
        if user_form.is_valid() and users_form.is_valid():
            user_form.save()
            users_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        users_form = UsersForm(instance=request.user.users)
    return render(request, 'registration/update.html', {
        'user_form': user_form,
        'users_form': users_form
    })


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        form_user_sys = UserCreationForm(request.POST)
        form_user = UserForm(request.POST)
        form_users = UsersForm(request.POST)
        if form_user.is_valid() and form_users.is_valid() and form_user_sys.is_valid():
            # save form in the memory not in database
            user_sys = form_user_sys.save(commit=False)  # системная форма
            user = form_user.save(commit=False)  # расширенная системная форма
            users = form_users.save(commit=False)  # дополненная форма пользователя
            user_sys.first_name = user.first_name  # переписываем данные из формы 2 в форму 1
            user_sys.last_name = user.last_name
            user_sys.email = user.email
            user_sys.save()  # сохраняем системную форму User
            users.user = user_sys
            users.save()  # сохраняем дополнительную форму Users
            login(request, user_sys, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('index')
    else:
        form_user_sys = UserCreationForm()
        form_user = UserForm()
        form_users = UsersForm()
    return render(request, 'registration/signup.html', {
        'form_user_sys': form_user_sys,
        'form_user': form_user,
        'form_users': form_users
    })

